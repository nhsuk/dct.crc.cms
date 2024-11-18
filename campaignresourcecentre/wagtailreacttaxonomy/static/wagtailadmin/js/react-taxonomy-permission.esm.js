import React, { createContext, useReducer, useContext, useState } from 'react';
import PropTypes from 'prop-types';
import { createUseStyles } from 'react-jss';

function _defineProperty(obj, key, value) {
  if (key in obj) {
    Object.defineProperty(obj, key, {
      value: value,
      enumerable: true,
      configurable: true,
      writable: true
    });
  } else {
    obj[key] = value;
  }

  return obj;
}

function ownKeys(object, enumerableOnly) {
  var keys = Object.keys(object);

  if (Object.getOwnPropertySymbols) {
    var symbols = Object.getOwnPropertySymbols(object);
    if (enumerableOnly) symbols = symbols.filter(function (sym) {
      return Object.getOwnPropertyDescriptor(object, sym).enumerable;
    });
    keys.push.apply(keys, symbols);
  }

  return keys;
}

function _objectSpread2(target) {
  for (var i = 1; i < arguments.length; i++) {
    var source = arguments[i] != null ? arguments[i] : {};

    if (i % 2) {
      ownKeys(Object(source), true).forEach(function (key) {
        _defineProperty(target, key, source[key]);
      });
    } else if (Object.getOwnPropertyDescriptors) {
      Object.defineProperties(target, Object.getOwnPropertyDescriptors(source));
    } else {
      ownKeys(Object(source)).forEach(function (key) {
        Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key));
      });
    }
  }

  return target;
}

function _slicedToArray(arr, i) {
  return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest();
}

function _arrayWithHoles(arr) {
  if (Array.isArray(arr)) return arr;
}

function _iterableToArrayLimit(arr, i) {
  if (typeof Symbol === "undefined" || !(Symbol.iterator in Object(arr))) return;
  var _arr = [];
  var _n = true;
  var _d = false;
  var _e = undefined;

  try {
    for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) {
      _arr.push(_s.value);

      if (i && _arr.length === i) break;
    }
  } catch (err) {
    _d = true;
    _e = err;
  } finally {
    try {
      if (!_n && _i["return"] != null) _i["return"]();
    } finally {
      if (_d) throw _e;
    }
  }

  return _arr;
}

function _unsupportedIterableToArray(o, minLen) {
  if (!o) return;
  if (typeof o === "string") return _arrayLikeToArray(o, minLen);
  var n = Object.prototype.toString.call(o).slice(8, -1);
  if (n === "Object" && o.constructor) n = o.constructor.name;
  if (n === "Map" || n === "Set") return Array.from(o);
  if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen);
}

function _arrayLikeToArray(arr, len) {
  if (len == null || len > arr.length) len = arr.length;

  for (var i = 0, arr2 = new Array(len); i < len; i++) arr2[i] = arr[i];

  return arr2;
}

function _nonIterableRest() {
  throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
}

var context = /*#__PURE__*/createContext();
var Provider = context.Provider;
/**
 * The Taxonomy context, available to all components. Use for user related data
 */

var TaxonomyContext = function TaxonomyContext(_ref) {
  var value = _ref.value,
      children = _ref.children;

  var _useReducer = useReducer(function (reducerState, action) {
    var taxonomyPermissionStore = reducerState.taxonomyPermissionStore,
        taxonomyPermissionJson = reducerState.taxonomyPermissionJson;

    switch (action.type) {
      case 'ADD':
        taxonomyPermissionStore[action.actionCode] = taxonomyPermissionStore[action.actionCode] || {};
        taxonomyPermissionStore[action.actionCode][action.groupCode] = taxonomyPermissionStore[action.actionCode][action.groupCode] || [];

        if (taxonomyPermissionStore[action.actionCode][action.groupCode].length === 1 && taxonomyPermissionStore[action.actionCode][action.groupCode][0] === '_all') {
          taxonomyPermissionStore[action.actionCode][action.groupCode] = [];
        }

        if (taxonomyPermissionStore[action.actionCode][action.groupCode].indexOf(action.item) === -1) {
          taxonomyPermissionStore[action.actionCode][action.groupCode].push(action.item);
        }

        taxonomyPermissionStore[action.actionCode][action.groupCode].sort();
        taxonomyPermissionJson.value = JSON.stringify(taxonomyPermissionStore);
        return _objectSpread2(_objectSpread2({}, reducerState), {}, {
          taxonomyPermissionStore: taxonomyPermissionStore
        });

      case 'REMOVE':
        taxonomyPermissionStore[action.actionCode][action.groupCode] = taxonomyPermissionStore[action.actionCode][action.groupCode].filter(function (item) {
          return item !== action.item;
        });

        if (taxonomyPermissionStore[action.actionCode][action.groupCode].length === 0) {
          taxonomyPermissionStore[action.actionCode][action.groupCode] = ['_all'];
        }

        taxonomyPermissionJson.value = JSON.stringify(taxonomyPermissionStore);
        return _objectSpread2(_objectSpread2({}, reducerState), {}, {
          taxonomyPermissionStore: taxonomyPermissionStore
        });

      case 'REMOVE_ALL_VOCABULARIES':
        taxonomyPermissionStore[action.actionCode][action.groupCode] = ['_all'];
        taxonomyPermissionJson.value = JSON.stringify(taxonomyPermissionStore);
        return _objectSpread2(_objectSpread2({}, reducerState), {}, {
          taxonomyPermissionStore: taxonomyPermissionStore
        });

      default:
        throw new Error('Unknown action');
    }
  }, value),
      _useReducer2 = _slicedToArray(_useReducer, 2),
      state = _useReducer2[0],
      dispatch = _useReducer2[1];

  var updatePermission = function updatePermission(actionCode, groupCode, item, remove) {
    if (remove) {
      dispatch({
        type: 'REMOVE',
        actionCode: actionCode,
        groupCode: groupCode,
        item: item
      });
    } else {
      dispatch({
        type: 'ADD',
        actionCode: actionCode,
        groupCode: groupCode,
        item: item
      });
    }
  };

  var removeAllVocabularies = function removeAllVocabularies(actionCode, groupCode) {
    dispatch({
      type: 'REMOVE_ALL_VOCABULARIES',
      actionCode: actionCode,
      groupCode: groupCode
    });
  };

  return /*#__PURE__*/React.createElement(Provider, {
    value: {
      state: state,
      action: {
        updatePermission: updatePermission,
        removeAllVocabularies: removeAllVocabularies
      }
    }
  }, children);
};

TaxonomyContext.propTypes = {
  value: PropTypes.shape({}),
  children: PropTypes.node.isRequired
};
TaxonomyContext.defaultProps = {
  value: {}
};

function useTaxonomyContext() {
  return useContext(context);
}

var useStyles = createUseStyles({
  vocabularyGroupSection: {
    '& label': {
      display: 'inline',
      float: 'initial',
      width: '100%'
    }
  }
});

function VocabularyGroup(props) {
  var taxonomyPermissionStore = useTaxonomyContext().state.taxonomyPermissionStore;

  var _useState = useState(true),
      _useState2 = _slicedToArray(_useState, 2),
      isAllChecked = _useState2[0],
      setIsAllChecked = _useState2[1];

  var _useTaxonomyContext$a = useTaxonomyContext().action,
      updatePermission = _useTaxonomyContext$a.updatePermission,
      removeAllVocabularies = _useTaxonomyContext$a.removeAllVocabularies;
  var classes = useStyles();
  var checkedCheckboxesCount = 0; // Use the json string data in the dom to define the default checkbox state

  function isChecked(itemCode) {
    if (props.actionCode in taxonomyPermissionStore && props.group.code in taxonomyPermissionStore[props.actionCode]) {
      if (taxonomyPermissionStore[props.actionCode][props.group.code].includes(itemCode)) {
        checkedCheckboxesCount += 1;

        if (isAllChecked) {
          setIsAllChecked(false);
        }

        return true;
      }
    }

    return false;
  } // Use the json string data in the dom to define the default 'all' checkbox state


  function updateAllChecked() {
    if (checkedCheckboxesCount > 0) {
      if (isAllChecked) {
        setIsAllChecked(false);
      }
    }

    if (!isAllChecked) {
      setIsAllChecked(true);
    }
  } // Update json string in the dom when user check/uncheck the checkbox


  function updateCheckboxPermission(e) {
    updatePermission(props.actionCode, props.group.code, e.target.value, !e.target.checked);

    if (e.target.checked) {
      checkedCheckboxesCount += 1;
    } else {
      checkedCheckboxesCount -= 1;
    }

    updateAllChecked();
  } // Update json string in the dom when user check/uncheck the checkbox


  function updateCheckboxAllPermission(e) {
    if (isAllChecked) {
      e.preventDefault();
    } else {
      props.group.children.forEach(function (item) {
        document.getElementById("checkbox-".concat(props.actionCode, "-").concat(props.group.code, "-").concat(item.code)).checked = false;
      });
      setIsAllChecked(true);
    }

    removeAllVocabularies(props.actionCode, props.group.code);
  }

  return /*#__PURE__*/React.createElement("div", {
    className: classes.vocabularyGroupSection
  }, /*#__PURE__*/React.createElement("h2", null, props.group.label), /*#__PURE__*/React.createElement("p", null, props.group.description), /*#__PURE__*/React.createElement("ul", null, /*#__PURE__*/React.createElement("div", {
    key: "div-".concat(props.actionCode, "-").concat(props.group.code, "-all")
  }, /*#__PURE__*/React.createElement("label", {
    htmlFor: "checkbox-".concat(props.actionCode, "-").concat(props.group.code, "-all")
  }, /*#__PURE__*/React.createElement("input", {
    id: "checkbox-".concat(props.actionCode, "-").concat(props.group.code, "-all"),
    onChange: updateCheckboxAllPermission,
    checked: isAllChecked,
    type: "checkbox"
  }), " All")), props.group.children && props.group.children.map(function (item) {
    return /*#__PURE__*/React.createElement("div", {
      key: "div-".concat(props.actionCode, "-").concat(props.group.code, "-").concat(item.code)
    }, /*#__PURE__*/React.createElement("label", {
      htmlFor: "checkbox-".concat(props.actionCode, "-").concat(props.group.code, "-").concat(item.code)
    }, /*#__PURE__*/React.createElement("input", {
      id: "checkbox-".concat(props.actionCode, "-").concat(props.group.code, "-").concat(item.code),
      onChange: updateCheckboxPermission,
      value: item.code,
      type: "checkbox",
      defaultChecked: isChecked(item.code)
    }), " ", item.label));
  })));
} // PropTypes


var vocabularyItemPropTypes = PropTypes.shape({
  label: PropTypes.string.isRequired,
  code: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired
});
vocabularyItemPropTypes.children = PropTypes.arrayOf(vocabularyItemPropTypes);
var vocabularyGroupPropTypes = PropTypes.shape({
  label: PropTypes.string.isRequired,
  code: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  children: PropTypes.arrayOf(vocabularyItemPropTypes)
});
VocabularyGroup.propTypes = {
  group: vocabularyGroupPropTypes,
  actionCode: PropTypes.string.isRequired
};
VocabularyGroup.defaultProps = {
  group: {}
};

var useStyles$1 = createUseStyles({
  modalBackground: {
    background: '#000',
    height: '100%',
    opacity: '0.8',
    position: 'fixed',
    right: '0',
    top: '0',
    width: '100%',
    zIndex: '98'
  },
  modalBox: {
    background: '#fff',
    border: '1px solid #000',
    borderRadius: 3,
    maxHeight: '80%',
    overflowY: 'auto',
    padding: '20px',
    position: 'fixed',
    right: 'calc(50% - 200px)',
    top: '50px',
    width: '400px',
    zIndex: '99',
    '& .closeBtn': {
      position: 'absolute',
      right: '10px',
      top: '10px',
      width: 'initial'
    }
  },
  btn: {
    width: 'initial'
  }
});

function TaxonomyPermissionChooser(props) {
  var _useState = useState(false),
      _useState2 = _slicedToArray(_useState, 2),
      showChooser = _useState2[0],
      setShowChooser = _useState2[1];

  var vocabularyGroups = useTaxonomyContext().state.vocabularyGroups;
  var classes = useStyles$1();

  function toggleChooser() {
    setShowChooser(!showChooser);
  }

  return /*#__PURE__*/React.createElement(React.Fragment, null, !showChooser && /*#__PURE__*/React.createElement("input", {
    className: classes.btn,
    onClick: toggleChooser,
    type: "button",
    value: "Edit"
  }), showChooser && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: classes.modalBackground
  }), /*#__PURE__*/React.createElement("div", {
    className: classes.modalBox
  }, /*#__PURE__*/React.createElement("input", {
    onClick: toggleChooser,
    className: "".concat(classes.btn, " closeBtn"),
    type: "button",
    value: "Close"
  }), vocabularyGroups && vocabularyGroups.map(function (group) {
    return /*#__PURE__*/React.createElement(VocabularyGroup, {
      key: "voc-".concat(props.actionCode, "-").concat(group.code),
      actionCode: props.actionCode,
      group: group
    });
  }))));
}

TaxonomyPermissionChooser.propTypes = {
  actionCode: PropTypes.string.isRequired
};

var useStyles$2 = createUseStyles({
  actionPanel: {
    backgroundColor: '#ddd',
    padding: '20px',
    marginTop: '20px'
  },
  '&.selected-term': {
    border: 'solid thin #333',
    borderRadius: 3
  },
  tags: {
    padding: 0,
    margin: 0,
    '& li': {
      display: 'inline-flex',
      flexWrap: 'nowrap',
      justifyContent: 'flex-start',
      alignContent: 'center',
      alignItems: 'stretch',
      margin: '5px 2px',
      fontSize: '1em',
      height: '1.5em',
      padding: 0,
      listStyle: 'none',
      fontFamily: 'sans-serif',
      '&.selected-term': {
        border: 'solid thin #333',
        borderRadius: 3
      },
      '&.message': {
        fontWeight: 'bold'
      },
      '& span.label': {
        display: 'flex',
        justifyContent: 'center',
        flexDirection: 'column',
        textAlign: 'center',
        flex: '1 1 auto',
        padding: [0, '1em'],
        whitespace: 'nowrap',
        background: '#fff'
      }
    }
  }
});

function TaxonomyPermissionAction(props) {
  var _useTaxonomyContext$s = useTaxonomyContext().state,
      vocabularyGroups = _useTaxonomyContext$s.vocabularyGroups,
      vocabularyLabels = _useTaxonomyContext$s.vocabularyLabels,
      taxonomyPermissionStore = _useTaxonomyContext$s.taxonomyPermissionStore;
  var classes = useStyles$2();
  var vocabularyTags = null;

  function renderActionGroupVocabulary(actionId, groupId) {
    var valueLabels = [];

    if (actionId in taxonomyPermissionStore && groupId in taxonomyPermissionStore[actionId]) {
      var values = taxonomyPermissionStore[actionId][groupId];
      values.filter(function (val) {
        return val !== '_all';
      }).forEach(function (value) {
        valueLabels.push(vocabularyLabels[value]);
      });
    }

    if (valueLabels.length > 0) {
      vocabularyTags = valueLabels.map(function (voc) {
        return /*#__PURE__*/React.createElement("li", {
          key: "".concat(actionId, "-").concat(groupId, "-").concat(voc),
          className: "selected-term"
        }, /*#__PURE__*/React.createElement("span", {
          className: "label"
        }, voc));
      });
    } else {
      vocabularyTags = /*#__PURE__*/React.createElement("li", {
        className: "message"
      }, "All");
    }

    return /*#__PURE__*/React.createElement("ul", {
      className: classes.tags
    }, vocabularyTags);
  }

  return /*#__PURE__*/React.createElement("div", {
    className: classes.actionPanel
  }, /*#__PURE__*/React.createElement("h2", null, props.action.label), /*#__PURE__*/React.createElement("ul", null, vocabularyGroups && vocabularyGroups.map(function (group) {
    return /*#__PURE__*/React.createElement("li", {
      key: "".concat(props.action.code, "-").concat(group.code)
    }, group.label, ": ", renderActionGroupVocabulary(props.action.code, group.code));
  })), /*#__PURE__*/React.createElement(TaxonomyPermissionChooser, {
    actionCode: props.action.code
  }));
} // PropTypes


var actionPropTypes = PropTypes.shape({
  label: PropTypes.string.isRequired,
  code: PropTypes.string.isRequired
});
TaxonomyPermissionAction.propTypes = {
  action: actionPropTypes
};
TaxonomyPermissionAction.defaultProps = {
  action: {}
};

var useStyles$3 = createUseStyles({
  globalPermissionsPanel: {
    backgroundColor: '#ddd',
    padding: '20px',
    '& label': {
      display: 'inline',
      float: 'initial',
      width: '100%'
    }
  },
  inheritPermissionPanel: {
    marginTop: '20px'
  },
  errorMessage: {
    backgroundColor: '#f5d6d7',
    borderRadius: '3px',
    padding: '20px'
  }
});

function TaxonomyPermissionPanel(props) {
  var _useState = useState(),
      _useState2 = _slicedToArray(_useState, 2),
      permission = _useState2[0],
      setPermission = _useState2[1];

  var _useState3 = useState(),
      _useState4 = _slicedToArray(_useState3, 2),
      inheritPermission = _useState4[0],
      setInheritPermission = _useState4[1];

  var gloablPermissionField = document.getElementById(props.globalPermissionFieldId);
  var inheritPermissionField = document.getElementById(props.inheritPermissionFieldId);
  var taxonomyPermissionJson = document.getElementById(props.taxonomyPermissionJsonId);
  var actions = props.actions.filter(function (action) {
    return props.permissionActions.includes(action.code);
  });
  var taxonomyPermissionStore = {};
  var errorMessages = [];
  var vocabularyLabels = {};
  var classes = useStyles$3();

  var _useState5 = useState(false),
      _useState6 = _slicedToArray(_useState5, 2),
      taxonomyPermissionInheritPageLoaded = _useState6[0],
      setTaxonomyPermissionInheritPageLoaded = _useState6[1];

  var _useState7 = useState(null),
      _useState8 = _slicedToArray(_useState7, 2),
      taxonomyPermissionInheritPageField = _useState8[0],
      setTaxonomyPermissionInheritPageField = _useState8[1];

  if (props.permissionType === 'page') {
    // check globalPermissionFieldId exists and get value
    if (props.globalPermissionFieldId) {
      if (gloablPermissionField) {
        if (gloablPermissionField.value && !permission) {
          setPermission(gloablPermissionField.value);
        }
      } else {
        errorMessages.push({
          code: "missing-elt-".concat(props.globalPermissionFieldId),
          text: "Missing element id: ".concat(props.globalPermissionFieldId)
        });
      }
    } else {
      errorMessages.push({
        code: "missing-id-".concat(props.globalPermissionFieldId),
        text: 'Missing globalPermissionFieldId'
      });
    } // check inheritPermissionFieldId exists and get value


    if (!taxonomyPermissionInheritPageLoaded) {
      if (props.inheritPermissionFieldId) {
        if (inheritPermissionField) {
          if (inheritPermissionField.value && !inheritPermission) {
            setInheritPermission(inheritPermissionField.value);
          }
        } else {
          errorMessages.push({
            code: "missing-elt-".concat(props.inheritPermissionFieldId),
            text: "Missing element id: ".concat(props.inheritPermissionFieldId)
          });
        }
      } else {
        errorMessages.push({
          code: "missing-id-".concat(props.inheritPermissionFieldId),
          text: 'Missing inheritPermissionFieldId'
        });
      }
    }
  } // check taxonomyPermissionJsonId exists and get value


  if (props.taxonomyPermissionJsonId) {
    if (taxonomyPermissionJson) {
      if (taxonomyPermissionJson.value) {
        taxonomyPermissionStore = JSON.parse(taxonomyPermissionJson.value);
      }
    } else {
      errorMessages.push({
        code: "missing-elt-".concat(props.taxonomyPermissionJsonId),
        text: "Missing element id: ".concat(props.taxonomyPermissionJsonId)
      });
    }
  } else {
    errorMessages.push({
      code: "missing-id-".concat(props.taxonomyPermissionJsonId),
      text: 'Missing taxonomyPermissionJsonId'
    });
  } // get vocabulary labels in context


  props.vocabularyGroups.forEach(function (group) {
    group.children.forEach(function (vocabulary) {
      vocabularyLabels[vocabulary.code] = vocabulary.label;
    });
  }); // init taxonomyPermissionJson

  actions.forEach(function (action) {
    if (!(action.code in taxonomyPermissionStore)) {
      taxonomyPermissionStore[action.code] = {};
    }

    props.vocabularyGroups.forEach(function (group) {
      if (!(group.code in taxonomyPermissionStore[action.code])) {
        taxonomyPermissionStore[action.code][group.code] = ['_all'];
      }
    });
  });
  taxonomyPermissionJson.value = JSON.stringify(taxonomyPermissionStore);

  function onChangeGlobalPermission(e) {
    setPermission(e.target.value);

    if (gloablPermissionField) {
      gloablPermissionField.value = e.target.value;
      inheritPermissionField.checked = true;
    }
  }

  function onChangeInheritPermission(e) {
    if (e.target.checked) {
      setInheritPermission('page');
      inheritPermissionField.checked = true;
      inheritPermissionField.value = 'page';
    } else {
      setInheritPermission('none');
      inheritPermissionField.checked = false;
      inheritPermissionField.value = 'none';
    }
  }

  return /*#__PURE__*/React.createElement(React.Fragment, null, errorMessages.length > 0 && /*#__PURE__*/React.createElement("ul", {
    className: classes.errorMessage
  }, errorMessages.map(function (msg) {
    return /*#__PURE__*/React.createElement("li", {
      key: msg.code
    }, msg.text);
  })), errorMessages.length === 0 && /*#__PURE__*/React.createElement(React.Fragment, null, props.permissionType === 'page' && /*#__PURE__*/React.createElement("p", null, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."), props.permissionType === 'model' && /*#__PURE__*/React.createElement("p", null, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."), props.permissionType === 'page' && /*#__PURE__*/React.createElement("div", {
    className: classes.globalPermissionsPanel
  }, /*#__PURE__*/React.createElement("label", {
    htmlFor: "radio_global_permission"
  }, "Global permission:", /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("label", {
    htmlFor: "radio_global_permission_public"
  }, /*#__PURE__*/React.createElement("input", {
    id: "radio_global_permission_public",
    onChange: onChangeGlobalPermission,
    type: "radio",
    name: "global-permission",
    value: "public",
    checked: permission === 'public'
  }), " Public"), /*#__PURE__*/React.createElement("label", {
    htmlFor: "radio_global_permission_restricted"
  }, /*#__PURE__*/React.createElement("input", {
    id: "radio_global_permission_restricted",
    onChange: onChangeGlobalPermission,
    type: "radio",
    name: "global-permission",
    value: "restricted",
    checked: permission === 'restricted'
  }), "Restricted"))), permission === 'restricted' && /*#__PURE__*/React.createElement("div", {
    className: classes.inheritPermissionPanel
  }, /*#__PURE__*/React.createElement("label", {
    htmlFor: "inheritPermission"
  }, /*#__PURE__*/React.createElement("input", {
    id: "inheritPermission",
    checked: inheritPermission === 'page',
    onChange: onChangeInheritPermission,
    type: "checkbox",
    name: "global-inherit-permission"
  }), "Inherit permission from another page")), permission === 'restricted' && inheritPermission === 'page' && props.taxonomyPermissionInheritPage && /*#__PURE__*/React.createElement("div", {
    ref: function ref(node) {
      if (node) {
        node.appendChild(props.taxonomyPermissionInheritPage);
        setTaxonomyPermissionInheritPageField(node);
        setTaxonomyPermissionInheritPageLoaded(true);
      }

      if (taxonomyPermissionInheritPageField) {
        taxonomyPermissionInheritPageField.appendChild(props.taxonomyPermissionInheritPage);
      }
    }
  })), (permission === 'restricted' || props.permissionType === 'model') && /*#__PURE__*/React.createElement(TaxonomyContext, {
    value: {
      vocabularyGroups: props.vocabularyGroups,
      taxonomyPermissionJson: taxonomyPermissionJson,
      vocabularyLabels: vocabularyLabels,
      taxonomyPermissionStore: taxonomyPermissionStore
    }
  }, props.actions && actions.map(function (action) {
    return /*#__PURE__*/React.createElement(TaxonomyPermissionAction, {
      key: "action-".concat(action.code),
      action: action
    });
  }))));
} // PropTypes


var actionPropTypes$1 = PropTypes.shape({
  label: PropTypes.string.isRequired,
  code: PropTypes.string.isRequired
});
var actionsPropTypes = PropTypes.arrayOf(actionPropTypes$1);
var vocabularyItemPropTypes$1 = PropTypes.shape({
  label: PropTypes.string.isRequired,
  code: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired
});
vocabularyItemPropTypes$1.children = PropTypes.arrayOf(vocabularyItemPropTypes$1);
var vocabularyGroupPropTypes$1 = PropTypes.shape({
  label: PropTypes.string.isRequired,
  code: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  children: PropTypes.arrayOf(vocabularyItemPropTypes$1)
});
var vocabularyGroupsPropTypes = PropTypes.arrayOf(vocabularyGroupPropTypes$1);
TaxonomyPermissionPanel.propTypes = {
  globalPermissionFieldId: PropTypes.string,
  inheritPermissionFieldId: PropTypes.string,
  taxonomyPermissionJsonId: PropTypes.string,
  taxonomyPermissionInheritPage: PropTypes.instanceOf(Element),
  actions: actionsPropTypes,
  vocabularyGroups: vocabularyGroupsPropTypes,
  permissionType: PropTypes.string,
  permissionActions: PropTypes.arrayOf(PropTypes.string)
};
TaxonomyPermissionPanel.defaultProps = {
  globalPermissionFieldId: null,
  inheritPermissionFieldId: null,
  taxonomyPermissionJsonId: null,
  taxonomyPermissionInheritPage: null,
  actions: [],
  vocabularyGroups: [],
  permissionType: 'page',
  permissionActions: []
};

export { TaxonomyPermissionPanel };
