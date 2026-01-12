from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from wagtail.models import Page


@login_required
def tag_management_results(request):
    """Display the results of a tag management bulk action"""
    
    # Get results from session
    results = request.session.pop('tag_management_results', None)
    
    if not results:
        # No results in session, redirect back to pages list
        return redirect('wagtailadmin_explore_root')
    
    # Get source page info if applicable
    source_page = None
    if results.get('source_page_id'):
        try:
            source_page = Page.objects.get(id=results['source_page_id']).specific
        except Page.DoesNotExist:
            pass
    
    context = {
        'change_details': results.get('change_details', []),
        'num_modified': results.get('num_modified', 0),
        'num_failed': results.get('num_failed', 0),
        'source_page': source_page,
    }
    
    return render(request, 'tag_management/results.html', context)
