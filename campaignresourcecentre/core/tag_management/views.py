from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from wagtail.models import Page

from campaignresourcecentre.campaigns.models import CampaignPage
from campaignresourcecentre.resources.models import ResourcePage
from .utils import get_page_taxonomy_tags


@login_required
def tag_management_results(request):
    """Display the results of a tag management bulk action"""

    # Get results from session
    results = request.session.pop("tag_management_results", None)

    if not results:
        # No results in session, redirect back to pages list
        return redirect("wagtailadmin_explore_root")

    # Get source page info if applicable
    source_page = None
    if results.get("source_page_id"):
        try:
            source_page = Page.objects.get(id=results["source_page_id"]).specific
        except Page.DoesNotExist:
            pass

    context = {
        "change_details": results.get("change_details", []),
        "num_modified": results.get("num_modified", 0),
        "num_failed": results.get("num_failed", 0),
        "source_page": source_page,
    }

    return render(request, "tag_management/results.html", context)


@require_GET
@login_required
def get_page_tags(request, page_id):
    """
    API endpoint to retrieve taxonomy tags for a given page.
    Returns JSON with the page's taxonomy tags organized by category.
    Works with both draft and published pages.
    """
    try:
        # Get the page in its latest revision state (draft or published)
        page = Page.objects.get(id=page_id).specific

        # For draft pages, get the latest revision
        if not page.live and page.has_unpublished_changes:
            latest_revision = page.get_latest_revision()
            if latest_revision:
                page = latest_revision.as_object()

        # Only allow CampaignPage or ResourcePage
        if not isinstance(page, (CampaignPage, ResourcePage)):
            return JsonResponse({"error": "Invalid page type"}, status=400)

        # Get taxonomy tags using utility function
        tags_list = get_page_taxonomy_tags(page)

        return JsonResponse(
            {
                "page_id": page_id,
                "page_title": page.title,
                "tags": tags_list,
                "is_draft": not page.live,
            }
        )

    except Page.DoesNotExist:
        return JsonResponse({"error": "Page not found"}, status=404)
    except Exception as e:
        print(f"DEBUG: Error in get_page_tags: {str(e)}")
        import traceback

        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)
