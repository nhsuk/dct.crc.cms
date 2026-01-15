document.addEventListener('DOMContentLoaded', () => {
    const tagsToRemove = {};
    const el = (id) => document.getElementById(id);
    const tagsToRemoveInput = el('id_tags_to_remove');
    const sourcePageInput = el('id_source_page');

    const fetchPageTags = async (pageId) => {
        const response = await fetch(`/crc-admin/tag-management/page/${pageId}/tags/`);
        if (!response.ok) throw new Error();
        const data = await response.json();
        return data.tags || [];
    };

    const renderTags = (tags, container) => {
        container.innerHTML = '';
        if (tags.length) {
            tags.forEach(tag => {
                const badge = document.createElement('span');
                badge.className = 'taxonomy-tag';
                badge.textContent = tag.label;
                container.appendChild(badge);
            });
        } else {
            const empty = document.createElement('em');
            empty.className = 'help-text';
            empty.textContent = 'No tags on selected page';
            container.appendChild(empty);
        }
    };

    const updateTagDisplay = async (pageId) => {
        const container = el('selected-page-tags-container');
        const display = el('selected-page-tags');
        if (!container || !display) return;
        
        try {
            const tags = await fetchPageTags(pageId);
            renderTags(tags, container);
            display.classList.add('visible');
        } catch {
            display.classList.remove('visible');
        }
    };


    if (tagsToRemoveInput) tagsToRemoveInput.value = '{}';

    if (sourcePageInput) {
        let lastPageId = sourcePageInput.value;
        new MutationObserver(() => {
            const pageId = sourcePageInput.value;
            if (pageId !== lastPageId) {
                lastPageId = pageId;
                if (pageId) updateTagDisplay(pageId);
                else el('selected-page-tags')?.classList.remove('visible');
            }
        }).observe(sourcePageInput, {attributes: true, attributeFilter: ['value']});
        
        if (lastPageId) updateTagDisplay(lastPageId);
    }

    document.querySelectorAll('.btn-remove').forEach(button => {
        button.addEventListener('click', e => {
            e.preventDefault();
            const {pageId, tagCode} = button.dataset;
            const badge = button.closest('.taxonomy-tag');
            
            badge.classList.toggle('removing');
            
            if (badge.classList.contains('removing')) {
                if (!tagsToRemove[pageId]) tagsToRemove[pageId] = [];
                tagsToRemove[pageId].push(tagCode);
            } else {
                const idx = tagsToRemove[pageId].indexOf(tagCode);
                tagsToRemove[pageId].splice(idx, 1);
                if (!tagsToRemove[pageId].length) delete tagsToRemove[pageId];
            }
            
            tagsToRemoveInput.value = JSON.stringify(tagsToRemove);
        });
    });
});
