document.addEventListener('DOMContentLoaded', () => {
    const tagsToRemoveInput = document.getElementById('id_tags_to_remove');
    const sourcePageInput = document.getElementById('id_source_page');
    const tagsToRemove = {};
    
    // Initialize the hidden input with empty object
    if (tagsToRemoveInput) {
        tagsToRemoveInput.value = JSON.stringify(tagsToRemove);
    }
    
    // Page chooser
    const chooseButton = document.getElementById('choose-source-page');
    if (chooseButton) {
        chooseButton.addEventListener('click', () => {
            const pageId = prompt('Enter page ID (temporary - will be replaced with proper chooser):');
            if (pageId) {
                sourcePageInput.value = pageId;
                document.getElementById('selected-page-title').textContent = `Page ID: ${pageId}`;
                document.getElementById('selected-page-display').style.display = 'block';
            }
        });
    }

    // Tag removal
    function updateRemovedTagsInput() {
        if (tagsToRemoveInput) {
            tagsToRemoveInput.value = JSON.stringify(tagsToRemove);
            console.log('Updated tags_to_remove:', tagsToRemoveInput.value);
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
    console.log('Found remove buttons:', removeButtons.length);
    
    removeButtons.forEach(button => {
        button.addEventListener('click', e => {
            e.preventDefault();
            e.stopPropagation();
            toggleTagRemoval(button);
        });
    });
    
    // Debug: Log form submission
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (e) => {
            console.log('Form submitting with:', {
                tags_to_remove: tagsToRemoveInput?.value,
                source_page: sourcePageInput?.value
            });
        });
    }
});
