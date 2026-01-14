document.addEventListener('DOMContentLoaded', () => {
    const tagsToRemoveInput = document.getElementById('id_tags_to_remove');
    const tagsToRemove = {};
    
    // Initialize the hidden input with empty object
    if (tagsToRemoveInput) {
        tagsToRemoveInput.value = JSON.stringify(tagsToRemove);
    }
    
    // Watch the hidden input field that stores the selected page ID
    const sourcePageInput = document.getElementById('id_source_page');
    
    if (sourcePageInput) {
        let lastPageId = sourcePageInput.value;
        
        // Use MutationObserver to watch for value changes
        const observer = new MutationObserver(() => {
            const pageId = sourcePageInput.value;
            
            // Only fetch if the value actually changed
            if (pageId !== lastPageId) {
                lastPageId = pageId;
                
                if (pageId) {
                    fetchAndDisplayPageTags(pageId);
                } else {
                    hideSelectedPageTags();
                }
            }
        });
        
        observer.observe(sourcePageInput, {
            attributes: true,
            attributeFilter: ['value']
        });
        
        // Check if a page is already selected on page load
        if (sourcePageInput.value) {
            fetchAndDisplayPageTags(sourcePageInput.value);
        }
    }
    
    function fetchAndDisplayPageTags(pageId) {
        // Use the proper API endpoint to get page tags
        fetch(`/crc-admin/tag-management/api/page-tags/${pageId}/`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch page tags');
            }
            return response.json();
        })
        .then(data => {
            if (data.tags && data.tags.length > 0) {
                displaySelectedPageTags(data.tags);
            } else {
                displayEmptyTags();
            }
        })
        .catch(err => {
            console.error('Error fetching page tags:', err);
            hideSelectedPageTags();
        });
    }
    
    function displaySelectedPageTags(tags) {
        const container = document.getElementById('selected-page-tags');
        const tagsContainer = document.getElementById('selected-page-tags-container');
        
        if (!container || !tagsContainer) return;
        
        tagsContainer.innerHTML = '';
        
        tags.forEach(tag => {
            const badge = document.createElement('span');
            badge.className = 'status-tag primary';
            badge.textContent = tag.label;
            tagsContainer.appendChild(badge);
        });
        
        container.classList.add('visible');
    }
    
    function displayEmptyTags() {
        const container = document.getElementById('selected-page-tags');
        const tagsContainer = document.getElementById('selected-page-tags-container');
        
        if (!container || !tagsContainer) return;
        
        tagsContainer.innerHTML = '<em class="help-text">No tags on selected page</em>';
        container.classList.add('visible');
    }
    
    function hideSelectedPageTags() {
        const container = document.getElementById('selected-page-tags');
        if (container) {
            container.classList.remove('visible');
        }
    }

    // Tag removal functionality
    function updateRemovedTagsInput() {
        if (tagsToRemoveInput) {
            tagsToRemoveInput.value = JSON.stringify(tagsToRemove);
        }
    }

    function updateNoTagsMessage(container) {
        const allTags = container.querySelectorAll('.tag-badge');
        const allRemoving = Array.from(allTags).every(tag => tag.classList.contains('removing'));
        let noTagsMsg = container.querySelector('.no-tags-message');
        
        if (allRemoving && !noTagsMsg) {
            noTagsMsg = document.createElement('em');
            noTagsMsg.className = 'no-tags-message';
            noTagsMsg.textContent = 'No tags (after save)';
            container.appendChild(noTagsMsg);
        } else if (!allRemoving && noTagsMsg) {
            noTagsMsg.remove();
        }
    }

    function toggleTagRemoval(button) {
        const {pageId, tagCode} = button.dataset;
        const tagBadge = button.closest('.tag-badge');
        const container = button.closest('.tags-container');
        
        if (tagBadge.classList.contains('removing')) {
            tagBadge.classList.remove('removing');
            const index = tagsToRemove[pageId]?.indexOf(tagCode);
            if (index > -1) {
                tagsToRemove[pageId].splice(index, 1);
                if (tagsToRemove[pageId].length === 0) {
                    delete tagsToRemove[pageId];
                }
            }
        } else {
            tagBadge.classList.add('removing');
            if (!tagsToRemove[pageId]) {
                tagsToRemove[pageId] = [];
            }
            tagsToRemove[pageId].push(tagCode);
        }
        
        updateRemovedTagsInput();
        updateNoTagsMessage(container);
    }

    // Attach listeners to all tag remove buttons
    const removeButtons = document.querySelectorAll('.tag-remove');
    
    removeButtons.forEach(button => {
        button.addEventListener('click', e => {
            e.preventDefault();
            e.stopPropagation();
            toggleTagRemoval(button);
        });
    });
});
