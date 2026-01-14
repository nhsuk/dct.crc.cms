
// [TODO]
// Leaving this in for now as i have made most of the functionality working except for the react state update part
// need to revisit this later to fully integrate with react state management
// possibly via custom events or direct state manipulation if feasible

const fetchTagsForPage = async (pageId) => {
  const response = await fetch(`/crc-admin/tag-management/page/${pageId}/tags/`);
  if (!response.ok) {
    throw new Error('Failed to fetch tags for the selected page');
  }
  const data = await response.json();
  return data.tags;
}

document.addEventListener('DOMContentLoaded', () => {
  const sourcePageInput = document.querySelector('[name="source_page"]');
  const copyTagsPreview = document.getElementById('copyTagsPreview');
  const copyTagsPreviewContainer = document.getElementById('copyTagsPreviewContainer');
  const copyTagsBtn = document.getElementById('copyTagsBtn');
  const taxonomyTextarea = document.querySelector('[name="taxonomy_json"]');
  const alertBox = document.getElementById('copyTagsMessage');
  let selectedPageTags = [];


  const onSourcePageChange = async (pageId) => {
    selectedPageTags = await fetchTagsForPage(pageId);
    const tagPreviewTemplate = document.getElementById('tagPreviewTemplate');

    copyTagsPreview.innerHTML = '';

    if (selectedPageTags.length === 0) {
      copyTagsPreview.textContent = "No tags found on the selected page.";
      return;
    }

    selectedPageTags.forEach(tag => {
      const tagElement = tagPreviewTemplate.content.cloneNode(true);
      tagElement.querySelector('.label').textContent = tag.label;
      copyTagsPreview.appendChild(tagElement);
    });


    copyTagsPreviewContainer.style.display = 'block';
  };


  const handleOnCopyTagsClicked = async () => {
    const operationMode = document.querySelector('[name="tag_operation_mode"]:checked').value;
    
    if(!sourcePageInput.value) {
      alertBox.textContent = 'Please select a source page to copy tags from.';
      alertBox.style.display = 'block';
      return;
    }

    if(selectedPageTags.length === 0) {
      alertBox.textContent = 'No tags to copy from the selected page.';
      alertBox.style.display = 'block';
      return;
    }

    if (!taxonomyTextarea) {
      alertBox.textContent = 'Tag taxonomy field not found.';
      alertBox.style.display = 'block';
      return;
    }

    alertBox.style.display = 'none';


    taxonomyTextarea.dispatchEvent(new Event('change', { bubbles: true }));
    taxonomyTextarea.dispatchEvent(new Event('input', { bubbles: true }));

    // currrent state of this.
    // Issue is that react is controlling this field and directly setting value doesn't work
    // so when we set the field value, it does not update the react state.

    // possible solution is to update the react state directly via a custom event or similar.
    // currently this is broken and does not work as intended. 
    // the code does update the textarea value but without the ui change. 
    // Clicking save without clicking on the taxonomy widget should save the changes with the updated value.


    if (operationMode === 'replace') {
      taxonomyTextarea.value = JSON.stringify(selectedPageTags);
    } else if (operationMode === 'merge') {
      const existingTags = await JSON.parse(taxonomyTextarea.value);
      const newTags = selectedPageTags.filter(tag => 
        !existingTags.some(existingTag => existingTag.code === tag.code)
      );
      const mergedTags = [...existingTags, ...newTags];
      taxonomyTextarea.innerHTML = JSON.stringify(mergedTags);
    }
  }

  copyTagsBtn.addEventListener('click', handleOnCopyTagsClicked);
    taxonomyTextarea.style.display = 'block'

  if (sourcePageInput) {
    sourcePageInput.addEventListener('change', (e) => onSourcePageChange(e.target.value));
  }
});
