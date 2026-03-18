import csv
import io
import json
from collections import Counter
from logging import getLogger

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from wagtail.models import Page

from campaignresourcecentre.wagtailreacttaxonomy.models import (
    load_campaign_topics,
    get_crc_taxonomy,
)

from .bulk_actions import BaseTagBulkAction

logger = getLogger(__name__)


class SetTopicTagsFromCsvBulkAction(BaseTagBulkAction):
    display_name = "Set Topic Tags from CSV"
    aria_label = "Set topic tags from CSV"
    action_type = "set_topic_tags_from_csv"


def _iter_taxonomy_terms(nodes):
    for node in nodes:
        if not isinstance(node, dict):
            continue

        if node.get("type") == "term":
            code = (node.get("code") or "").strip()
            label = (node.get("label") or "").strip()
            if code and label:
                yield {"code": code, "label": label}

        children = node.get("children") or []
        if isinstance(children, list):
            yield from _iter_taxonomy_terms(children)


def _build_tag_lookup():
    data = get_crc_taxonomy()
    load_campaign_topics(data)

    tags_by_code = {}
    tags_by_label = {}
    ambiguous_labels = set()

    for tag in _iter_taxonomy_terms(data):
        tags_by_code[tag["code"].casefold()] = tag

        label_key = tag["label"].casefold()
        existing = tags_by_label.get(label_key)
        if existing and existing["code"] != tag["code"]:
            ambiguous_labels.add(label_key)
            continue

        if label_key not in ambiguous_labels:
            tags_by_label[label_key] = tag

    for label_key in ambiguous_labels:
        tags_by_label.pop(label_key, None)

    return tags_by_code, tags_by_label, ambiguous_labels


def _parse_csv_rows(uploaded_file):
    try:
        csv_data = uploaded_file.read().decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValidationError("CSV file must be UTF-8 encoded") from exc

    rows = []
    reader = csv.reader(io.StringIO(csv_data))
    for row_number, row in enumerate(reader, start=1):
        if not row or not any(cell.strip() for cell in row):
            continue

        page_id_raw = row[0].strip()
        if row_number == 1 and page_id_raw.casefold() in {"page_id", "id"}:
            continue

        tag_names = []
        for cell in row[1:]:
            cell = cell.strip()
            if not cell:
                continue

            tag_names.extend(
                token.strip() for token in cell.split(",") if token.strip()
            )

        rows.append(
            {
                "row_number": row_number,
                "page_id_raw": page_id_raw,
                "tag_names": tag_names,
            }
        )

    if not rows:
        raise ValidationError("CSV file is empty")

    return rows


def _resolve_tags(tag_names, tags_by_code, tags_by_label, ambiguous_labels):
    resolved_tags = []
    seen_codes = set()
    unknown_tags = []
    ambiguous_tag_labels = []

    for tag_name in tag_names:
        key = tag_name.casefold()

        if key in tags_by_code:
            tag = tags_by_code[key]
        elif key in tags_by_label:
            tag = tags_by_label[key]
        elif key in ambiguous_labels:
            ambiguous_tag_labels.append(tag_name)
            continue
        else:
            unknown_tags.append(tag_name)
            continue

        code = tag["code"]
        if code not in seen_codes:
            resolved_tags.append(tag)
            seen_codes.add(code)

    errors = []
    if unknown_tags:
        unknown_list = ", ".join(sorted(set(unknown_tags), key=str.casefold))
        errors.append(f"Unknown tags: {unknown_list}")

    if ambiguous_tag_labels:
        ambiguous_list = ", ".join(sorted(set(ambiguous_tag_labels), key=str.casefold))
        errors.append(f"Ambiguous tag labels: {ambiguous_list}")

    if errors:
        raise ValidationError(" ".join(errors))

    return resolved_tags


def _merge_topic_tags(existing_tags, topic_tags, topic_codes):
    non_topic_tags = [
        tag for tag in (existing_tags or []) if tag.get("code") not in topic_codes
    ]
    return non_topic_tags + topic_tags


def _has_csv_tag_permission(user):
    return user.is_superuser


def _process_row(
    row,
    pages_by_id,
    action,
    tags_by_code,
    tags_by_label,
    ambiguous_labels,
    topic_codes,
    user,
):
    """Process one CSV row and return (outcome, result_dict).

    outcome is one of: 'modified', 'unchanged', 'failed'.
    """
    row_number = row["row_number"]
    page_id_raw = row["page_id_raw"]

    error = lambda message: {
        "row": row_number,
        "page_id": page_id_raw,
        "status": "error",
        "error": message,
    }

    try:
        page_id = int(page_id_raw)
    except (TypeError, ValueError):
        return "failed", error(f"Invalid page ID '{page_id_raw}'")

    page = pages_by_id.get(page_id)
    if page is None:
        return "failed", error(f"Page with ID {page_id} was not found")

    if not action.check_perm(page):
        return "failed", error("Only campaign and resource pages can be updated")

    try:
        resolved_tags = _resolve_tags(
            row["tag_names"], tags_by_code, tags_by_label, ambiguous_labels
        )
        topic_tags = [tag for tag in resolved_tags if tag["code"] in topic_codes]
        action._ensure_has_topic_tag(topic_tags, topic_codes, action_type="add")

        live_tags = _merge_topic_tags(
            action._get_current_tags(page), topic_tags, topic_codes
        )

        draft_tags = None
        if action._has_unpublished_changes(page):
            draft_tags = _merge_topic_tags(
                action._get_draft_tags(page), topic_tags, topic_codes
            )

        has_changes = action._save_tags(page, live_tags, draft_tags, user)
    except ValidationError as exc:
        error_message = " ".join(exc.messages)
        logger.error(
            "CSV tag update validation error for page ID %s: %s", page.id, error_message
        )
        return "failed", error(error_message)

    except Exception as exc:
        logger.error("CSV tag update failed for page ID %s: %s", page.id, exc)
        return "failed", error(
            "An unexpected error occurred while updating tags for this page"
        )

    outcome = "modified" if has_changes else "unchanged"
    status = "updated" if has_changes else "unchanged"
    return outcome, {
        "row": row_number,
        "page_id": page.id,
        "status": status,
        "tags": live_tags,
    }


@csrf_exempt
@require_http_methods(["POST"])
def set_topic_tags_from_csv(request):
    if not _has_csv_tag_permission(request.user):
        raise PermissionDenied

    uploaded_file = request.FILES.get("file") or request.FILES.get("csv_file")
    if not uploaded_file:
        return JsonResponse(
            {"detail": "Please upload a CSV file using the 'file' form field."},
            status=400,
        )

    action = object.__new__(SetTopicTagsFromCsvBulkAction)

    try:
        rows = _parse_csv_rows(uploaded_file)
        tags_by_code, tags_by_label, ambiguous_labels = _build_tag_lookup()
        topic_codes = action._get_topic_codes()
    except ValidationError as exc:
        return JsonResponse({"detail": " ".join(exc.messages)}, status=400)

    valid_page_ids = []
    for row in rows:
        try:
            valid_page_ids.append(int(row["page_id_raw"]))
        except (TypeError, ValueError):
            continue

    pages_by_id = {
        page.id: page for page in Page.objects.filter(id__in=valid_page_ids).specific()
    }

    counts = Counter()
    results = []

    for row in rows:
        outcome, result = _process_row(
            row,
            pages_by_id,
            action,
            tags_by_code,
            tags_by_label,
            ambiguous_labels,
            topic_codes,
            request.user,
        )
        results.append(result)
        counts[outcome] += 1

    response_payload = {
        "num_processed": len(rows),
        "num_modified": counts["modified"],
        "num_unchanged": counts["unchanged"],
        "num_failed": counts["failed"],
        "results": results,
    }

    return JsonResponse(response_payload)
