import withStyles from 'react-jss';
import PropTypes from 'prop-types';
import React, { Component } from 'react';

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _defineProperties(target, props) {
  for (var i = 0; i < props.length; i++) {
    var descriptor = props[i];
    descriptor.enumerable = descriptor.enumerable || false;
    descriptor.configurable = true;
    if ("value" in descriptor) descriptor.writable = true;
    Object.defineProperty(target, descriptor.key, descriptor);
  }
}

function _createClass(Constructor, protoProps, staticProps) {
  if (protoProps) _defineProperties(Constructor.prototype, protoProps);
  if (staticProps) _defineProperties(Constructor, staticProps);
  return Constructor;
}

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError("Super expression must either be null or a function");
  }

  subClass.prototype = Object.create(superClass && superClass.prototype, {
    constructor: {
      value: subClass,
      writable: true,
      configurable: true
    }
  });
  if (superClass) _setPrototypeOf(subClass, superClass);
}

function _getPrototypeOf(o) {
  _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) {
    return o.__proto__ || Object.getPrototypeOf(o);
  };
  return _getPrototypeOf(o);
}

function _setPrototypeOf(o, p) {
  _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) {
    o.__proto__ = p;
    return o;
  };

  return _setPrototypeOf(o, p);
}

function _assertThisInitialized(self) {
  if (self === void 0) {
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  }

  return self;
}

function _possibleConstructorReturn(self, call) {
  if (call && (typeof call === "object" || typeof call === "function")) {
    return call;
  }

  return _assertThisInitialized(self);
}

function _toConsumableArray(arr) {
  return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _nonIterableSpread();
}

function _arrayWithoutHoles(arr) {
  if (Array.isArray(arr)) {
    for (var i = 0, arr2 = new Array(arr.length); i < arr.length; i++) arr2[i] = arr[i];

    return arr2;
  }
}

function _iterableToArray(iter) {
  if (Symbol.iterator in Object(iter) || Object.prototype.toString.call(iter) === "[object Arguments]") return Array.from(iter);
}

function _nonIterableSpread() {
  throw new TypeError("Invalid attempt to spread non-iterable instance");
}

var styles = function styles(theme) {
  return {
    root: {
      '& .term': {
        margin: '5px 0'
      },
      '& .accordion': {
        backgroundColor: '#eee',
        color: '#000',
        cursor: 'pointer',
        padding: '18px',
        width: '100%',
        border: 'none',
        textAlign: 'left',
        outline: 'none',
        fontSize: '15px',
        transition: '0.4s',
        boxSizing: 'border-box',
        '& small': {
          display: 'block',
          marginLeft: '14px'
        },
        '&:before': {
          content: '"+"',
          color: '#777',
          fontWeight: 'bold',
          float: 'left',
          marginRight: '5px'
        },
        '&:hover': {
          backgroundColor: '#ccc'
        },
        '&.active': {
          backgroundColor: '#ccc',
          '&:before': {
            content: '"‒"'
          }
        }
      },
      '& .panel': {
        padding: '0 54px',
        display: 'none',
        color: '#000',
        backgroundColor: '#ddd',
        overflow: 'hidden',
        '& .term': {
          '& .panel': {
            display: 'block'
          }
        },
        '& .accordion': {
          padding: 0,
          backgroundColor: 'transparent',
          marginLeft: '-13px',
          '&:hover': {
            backgroundColor: 'transparent'
          },
          '&.active': {
            backgroundColor: 'transparent'
          }
        }
      }
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
        background: '#fff',
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
          whitespace: 'nowrap'
        },
        '& span.remove': {
          display: 'flex',
          justifyContent: 'center',
          flexDirection: 'column',
          textAlign: 'center',
          flex: '0 1 auto',
          padding: [0, '0.8em'],
          margin: 0,
          cursor: 'pointer',
          backgroundColor: '#e4e4e4',
          borderTopRightRadius: 3,
          borderBottomRightRadius: 3
        }
      }
    }
  };
};

var Taxonomy =
/*#__PURE__*/
function (_Component) {
  _inherits(Taxonomy, _Component);

  function Taxonomy(props) {
    var _this;

    _classCallCheck(this, Taxonomy);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(Taxonomy).call(this, props));

    _this.parseTerms = function (taxoTerms) {
      var assignedTaxo = _this.state.assignedTaxo;
      var taxo = [];

      for (var i = 0; i < taxoTerms.length; i++) {
        var value = taxoTerms[i];
        var terms = [];
        var attr = {
          type: "checkbox",
          value: value['code'],
          name: value['label'],
          onChange: function onChange(e) {
            return _this.handleChecked(e);
          }
        };

        if (assignedTaxo) {
          for (var a = 0; a < assignedTaxo.length; a++) {
            if (assignedTaxo[a]['code'] === value['code']) {
              attr['checked'] = true;
            }
          }
        }

        if (Array.isArray(value['children']) && value['children'].length > 0) {
          var item = [],
              clss = 'accordion';

          if (value['type'] === 'vocabulary') {
            item.push(React.createElement("strong", null, value['label']));
            item.push(React.createElement("small", null, value['description']));
          } else {
            item.push(React.createElement("input", attr));
            item.push(React.createElement("label", null, value['label']));
            clss += ' active';
          }

          terms.push(React.createElement("div", {
            key: i,
            className: "term"
          }, React.createElement("div", {
            className: clss,
            onClick: function onClick(e) {
              return _this.handleAccordion(e);
            }
          }, item), React.createElement("div", {
            className: "panel"
          }, _this.parseTerms(value['children']))));
        } else {
          terms.push(React.createElement("div", {
            key: i,
            className: "term"
          }, React.createElement("input", attr), React.createElement("label", null, value['code'])));
        }

        taxo.push(terms);
      }

      return taxo;
    };

    _this.handleChecked = function (e) {
      var checkboxElem = e.currentTarget;
      var selectedTerms = _this.state.assignedTaxo;

      if (checkboxElem.checked) {
        selectedTerms = [].concat(_toConsumableArray(selectedTerms), [{
          code: checkboxElem.getAttribute('value'),
          label: checkboxElem.getAttribute('name')
        }]);
      } else {
        selectedTerms = selectedTerms.filter(function (item) {
          return item.code !== checkboxElem.getAttribute('value');
        });
      }

      _this.setState({
        assignedTaxo: selectedTerms
      }); // var target = document.querySelector(`#${this.props.outputFieldId}`);


      var outputFieldElem = document.getElementById(_this.props.outputFieldId);

      if (outputFieldElem) {
        outputFieldElem.innerHTML = JSON.stringify(selectedTerms);
      }
    };

    _this.handleAccordion = function (e) {
      // Toggle the accordion only if the user didn't click on thecheckbox.
      if (!e.target.type || e.target.type !== 'checkbox') {
        var target = e.currentTarget;
        var panel = target.nextElementSibling;
        target.classList.toggle("active");

        if (target.classList.contains("active")) {
          panel.style.display = "block";
        } else {
          panel.style.display = "none";
        }
      }
    };

    _this.getAssignedTaxonomy = function () {
      var assignedTaxo = _this.state.assignedTaxo;

      if (!assignedTaxo) {
        var target = document.querySelector("#".concat(_this.props.outputFieldId));

        try {
          assignedTaxo = JSON.parse(target.innerHTML);

          _this.setState({
            assignedTaxo: assignedTaxo
          });
        } catch (e) {}
      }
    };

    _this.parseAssignedTaxonomy = function (taxoTerms) {
      var assignedTaxo = _this.state.assignedTaxo;
      var tags = [];

      if (Array.isArray(assignedTaxo)) {
        for (var a = 0; a < assignedTaxo.length; a++) {
          tags.push(React.createElement("li", {
            key: a,
            className: "selected-term"
          }, React.createElement("span", {
            className: "label"
          }, assignedTaxo[a]['label']), React.createElement("span", {
            className: "remove",
            rel: assignedTaxo[a]['code'],
            onClick: function onClick(e) {
              return _this.removeAssignedTaxonomy(e);
            }
          }, "x")));
        }
      }

      return tags.length > 0 ? tags : null;
    };

    _this.removeAssignedTaxonomy = function (e) {
      var assignedTaxo = _this.state.assignedTaxo;
      var taxCode = e.currentTarget.getAttribute('rel');
      var newAssignedTaxo = [];

      for (var i = 0; i < assignedTaxo.length; i++) {
        if (assignedTaxo[i]['code'] != taxCode) {
          newAssignedTaxo.push({
            code: assignedTaxo[i]['code'],
            label: assignedTaxo[i]['label']
          });
        }
      }

      document.querySelector("#".concat(_this.props.outputFieldId)).innerHTML = JSON.stringify(newAssignedTaxo);

      _this.setState({
        assignedTaxo: newAssignedTaxo
      });
    };

    _this.ref = React.createRef();
    _this.handleAccordion = _this.handleAccordion.bind();
    _this.removeAssignedTaxonomy = _this.removeAssignedTaxonomy.bind();
    _this.state = {
      assignedTaxo: ''
    };
    return _this;
  }

  _createClass(Taxonomy, [{
    key: "render",
    value: function render() {
      var _this$props = this.props,
          id = _this$props.id,
          classes = _this$props.classes,
          style = _this$props.style,
          className = _this$props.className,
          taxonomyTerms = _this$props.taxonomyTerms,
          outputFieldId = _this$props.outputFieldId,
          termsDisplayText = _this$props.termsDisplayText,
          assignedDisplayText = _this$props.assignedDisplayText;
      this.getAssignedTaxonomy();
      return React.createElement("div", {
        id: id,
        ref: this.ref,
        className: "".concat(classes.root, " ").concat(className),
        style: style
      }, assignedDisplayText, React.createElement("ul", {
        className: classes.tags
      }, this.parseAssignedTaxonomy(taxonomyTerms) || React.createElement("li", {
        className: "message"
      }, "No keywords selected")), termsDisplayText, React.createElement("div", {
        className: "term-chooser"
      }, this.parseTerms(taxonomyTerms)));
    }
  }]);

  return Taxonomy;
}(Component);

Taxonomy.defaultProps = {
  taxonomyTerms: [],
  outputFieldId: "",
  termsDisplayText: "Choose from the following keywords:",
  assignedDisplayText: "Selected keywords"
};
Taxonomy.propTypes = {
  id: PropTypes.string,
  className: PropTypes.string,
  style: PropTypes.object,
  taxonomyTerms: PropTypes.array.isRequired,
  outputFieldId: PropTypes.string.isRequired,
  termsDisplayText: PropTypes.string,
  assignedDisplayText: PropTypes.string
};
var Taxonomy$1 = withStyles(styles, {
  injectTheme: true
})(Taxonomy);

export default Taxonomy$1;
