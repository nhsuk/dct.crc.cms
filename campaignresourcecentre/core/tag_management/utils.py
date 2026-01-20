import json


def get_page_taxonomy_tags(page):
    taxonomy_json = getattr(page, "taxonomy_json", None)
    data = None

    if taxonomy_json:
        try:
            data = json.loads(taxonomy_json)
        except (json.JSONDecodeError, TypeError):
            pass
    else:
        data = getattr(page, "taxonomy", [])

    if isinstance(data, list):
        return [{"code": t.get("code", ""), "label": t.get("label", "")} for t in data]

    return []
