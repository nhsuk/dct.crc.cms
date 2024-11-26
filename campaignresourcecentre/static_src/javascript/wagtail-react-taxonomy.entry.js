import ReactDOM from 'react-dom';
import { ThemeProvider } from 'react-jss';

import Taxonomy from './react-taxonomy.esm.js';
import { TaxonomyPermissionPanel } from './react-taxonomy-permission.esm.js';

window.onload = function (){

  // load  taxonomy terms chooser
  if (document.getElementById('taxonomy-terms-json')) {
    const taxonomyTerms = document.getElementById('taxonomy-terms-json').value;
    const taxonomyTermsJson = JSON.parse(taxonomyTerms);
    ReactDOM.render(
      <ThemeProvider theme={{}}>
        <Taxonomy
          outputFieldId="id_taxonomy_json"
          taxonomyTerms={taxonomyTermsJson}
          termsDisplayText="Choose from the following keywords:"
          assignedDisplayText="Selected keywords"
        />
      </ThemeProvider>,
      document.getElementById('react-taxonomy')
    );
  }

  // load  taxonomy permission panel
  if (document.getElementById('permission-terms-json')) {
    const taxonomyPermission = document.getElementById('permission-terms-json').value;
    const taxonomyPermissionJson = JSON.parse(taxonomyPermission);
    const actions = taxonomyPermissionJson.actions;
    const vocabularyGroups = taxonomyPermissionJson.vocabularyGroups;
    let permissionActions = null;
    let taxonomyPermissionInheritPage = null;
    let permissionType = 'page';
    if (document.getElementById('id_permission_inherit_page-chooser')) {
      taxonomyPermissionInheritPage = document.getElementById('id_permission_inherit_page-chooser').closest('.field');
      taxonomyPermissionInheritPage.closest('.object').style.display = 'none';
    }
    if (document.getElementById('permission-actions')) {
      const permissionActionsElt = document.getElementById('permission-actions');
      permissionActionsElt.style.display = 'none';
      permissionActions = JSON.parse(permissionActionsElt.value);
    }
    if (document.getElementById('permission-type')) {
      const permissionTypeElt = document.getElementById('permission-type');
      permissionTypeElt.style.display = 'none';
      permissionType = permissionTypeElt.value;
    }
    ReactDOM.render(
      <TaxonomyPermissionPanel
        actions={actions}
        vocabularyGroups={vocabularyGroups}
        globalPermissionFieldId="id_global_permission"
        inheritPermissionFieldId="id_inherit_permission"
        taxonomyPermissionJsonId="id_permissions_json"
        taxonomyPermissionInheritPage={taxonomyPermissionInheritPage}
        permissionActions={permissionActions}
        permissionType={permissionType}
      />,
      document.getElementById('react-taxonomy-permissions')
    );
  };
};
