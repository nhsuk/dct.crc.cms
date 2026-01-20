document.addEventListener('DOMContentLoaded', () => {
    const tagsToRemove = {};
    const tagsToRemoveInput = document.getElementById('id_tags_to_remove');
    if (tagsToRemoveInput) tagsToRemoveInput.value = '{}';

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
