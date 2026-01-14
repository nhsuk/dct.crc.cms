"""
Utility functions for tag management.
"""
import json


def get_page_taxonomy_tags(page):
    """
    Extract taxonomy tags from a page in a standardized format.
    
    Returns a list of dicts with 'code' and 'label' keys.
    Handles both taxonomy and taxonomy_json fields.
    
    Args:
        page: A CampaignPage or ResourcePage instance
        
    Returns:
        list: List of tag dicts [{'code': 'X', 'label': 'Y'}, ...]
    """
    # Try taxonomy_json field first (stored format)
    if hasattr(page, 'taxonomy_json') and page.taxonomy_json:
        try:
            taxonomy_data = json.loads(page.taxonomy_json)
            if isinstance(taxonomy_data, list):
                return [
                    {
                        'code': tag.get('code', ''),
                        'label': tag.get('label', ''),
                    }
                    for tag in taxonomy_data
                ]
        except (json.JSONDecodeError, TypeError, AttributeError):
            pass
    
    # Fallback to taxonomy field (live field value)
    if hasattr(page, 'taxonomy'):
        taxonomy = page.taxonomy
        if isinstance(taxonomy, list) and taxonomy:
            return [
                {
                    'code': tag.get('code', ''),
                    'label': tag.get('label', ''),
                }
                for tag in taxonomy
            ]
    
    return []
