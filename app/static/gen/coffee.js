var Quizlet, clone, q, zip,
  __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

String.prototype.strip = function() {
  if (String.prototype.trim != null) {
    return this.trim();
  } else {
    return this.replace(/^\s+|\s+$/g, "");
  }
};

String.prototype.lstrip = function() {
  return this.replace(/^\s+/g, "");
};

String.prototype.rstrip = function() {
  return this.replace(/\s+$/g, "");
};

Array.prototype.toDict = function(key) {
  return this.reduce((function(dict, obj) {
    if (obj[key] != null) {
      dict[obj[key]] = obj;
    }
    return dict;
  }), {});
};

clone = function(obj) {
  var flags, key, newInstance;
  if ((obj == null) || typeof obj !== 'object') {
    return obj;
  }
  if (obj instanceof Date) {
    return new Date(obj.getTime());
  }
  if (obj instanceof RegExp) {
    flags = '';
    if (obj.global != null) {
      flags += 'g';
    }
    if (obj.ignoreCase != null) {
      flags += 'i';
    }
    if (obj.multiline != null) {
      flags += 'm';
    }
    if (obj.sticky != null) {
      flags += 'y';
    }
    return new RegExp(obj.source, flags);
  }
  newInstance = new obj.constructor();
  for (key in obj) {
    newInstance[key] = clone(obj[key]);
  }
  return newInstance;
};

zip = function() {
  var arr, i, length, lengthArray, _i, _results;
  lengthArray = (function() {
    var _i, _len, _results;
    _results = [];
    for (_i = 0, _len = arguments.length; _i < _len; _i++) {
      arr = arguments[_i];
      _results.push(arr.length);
    }
    return _results;
  }).apply(this, arguments);
  length = Math.min.apply(Math, lengthArray);
  _results = [];
  for (i = _i = 0; 0 <= length ? _i < length : _i > length; i = 0 <= length ? ++_i : --_i) {
    _results.push((function() {
      var _j, _len, _results1;
      _results1 = [];
      for (_j = 0, _len = arguments.length; _j < _len; _j++) {
        arr = arguments[_j];
        _results1.push(arr[i]);
      }
      return _results1;
    }).apply(this, arguments));
  }
  return _results;
};

$.q = {
  $decks: $("#decks"),
  $filter: $("#filter")
};

q = $.q;

Quizlet = (function() {
  Quizlet.prototype.baseUrl = "https://api.quizlet.com/2.0";

  Quizlet.prototype.key = "client_id=2xvUtAyRyn";

  Quizlet.prototype.decks = {};

  Quizlet.prototype.decks_by_id = lunr(function() {
    this.field("terms");
    this.field("definitions");
    this.field("title");
    this.field("description");
    return this.ref("id");
  });

  Quizlet.prototype.collectedIds = [];

  function Quizlet() {
    this.template = Handlebars.compile($("#deckTemplate").html());
    this.show_only = function(ids) {
      debugger;
      var deck, x, _i, _len, _ref, _ref1, _results;
      _ref = $(".deck");
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        deck = _ref[_i];
        x = $(deck);
        if (_ref1 = deck.attributes["data-qid"], __indexOf.call(ids, _ref1) < 0) {
          _results.push($(deck).hide());
        } else {
          _results.push($(deck).show());
        }
      }
      return _results;
    };
    this.getDecks = function(term) {
      if (term) {
        return $.getJSON("/decks/" + term, (function(_this) {
          return function(data) {
            var deck, x, _i, _len, _results;
            x = clone(data);
            _this.populate(x);
            _results = [];
            for (_i = 0, _len = data.length; _i < _len; _i++) {
              deck = data[_i];
              _results.push(_this.add_to_lunr(deck.json));
            }
            return _results;
          };
        })(this));
      }
    };
    this.populate = function(data) {
      var deckContext;
      deckContext = {
        decks: data
      };
      return q.$decks.append(this.template(deckContext));
    };
    this.add_to_lunr = function(deck) {
      var definitions, formated_deck, term;
      formated_deck = {
        terms: ((function() {
          var _i, _len, _ref, _results;
          _ref = deck.terms;
          _results = [];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            term = _ref[_i];
            _results.push(term);
          }
          return _results;
        })()).join(' '),
        definitions: ((function() {
          var _i, _len, _ref, _results;
          _ref = deck.terms;
          _results = [];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            definitions = _ref[_i];
            _results.push(definitions);
          }
          return _results;
        })()).join(' '),
        title: deck.title,
        description: deck.description,
        id: deck.id
      };
      return this.decks_by_id.add(formated_deck);
    };
    $("#getDecks").submit((function(_this) {
      return function(e) {
        var x, _i, _len, _ref;
        _this.terms = (function() {
          var _i, _len, _ref, _results;
          _ref = $("#specificKeyword").val().split(",");
          _results = [];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            x = _ref[_i];
            _results.push(x.trim());
          }
          return _results;
        })();
        _ref = _this.terms;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          x = _ref[_i];
          _this.getDecks(x);
        }
        return e.preventDefault();
      };
    })(this));
    q.mousedown = function(e) {
      e.preventDefault();
      q.md = true;
      q.selected = $(this).hasClass("selected");
      return q.mouseover(e);
    };
    q.mouseover = function(e) {
      e.preventDefault();
      if (q.md === true && q.selected === $(this).hasClass("selected")) {
        return $(this).toggleClass("selected");
      }
    };
    q.mouseup = function(e) {
      e.preventDefault();
      return q.md = false;
    };
    q.mouseleave = function(e) {
      q.md = false;
      return q.selected = false;
    };
    q.$decks.on("click", ".card", function(e) {
      return $(this).toggleClass("selected");
    }).on("mouseover", ".card", q.mouseover).on("mousedown", ".card", q.mousedown).on("mouseup", ".card", q.mouseup).on("mouseleave", ".deck", q.mouseleave);
    $("#reset").on("click", function(e) {
      e.preventDefault();
      return q.$decks.empty();
    });
    q.$decks.on("click", ".removeDeck", function(e) {
      return e.currentTarget.parentElement.remove();
    });
    $("#export").click(function(e) {
      var cards, definition, definitions, term, terms;
      terms = (function() {
        var _i, _len, _ref, _results;
        _ref = $(".card.selected .term");
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          term = _ref[_i];
          _results.push(term.textContent);
        }
        return _results;
      })();
      definitions = (function() {
        var _i, _len, _ref, _results;
        _ref = $(".card.selected .definition");
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          definition = _ref[_i];
          _results.push(definition.textContent);
        }
        return _results;
      })();
      cards = zip(terms, definitions);
      return console.log(terms, definitions, cards);
    });
    $("#filterDecks").submit((function(_this) {
      return function(e) {
        var d, deck, decks_with_filter_terms, filter_terms, x, _i, _j, _len, _len1, _ref, _ref1, _results, _results1;
        e.preventDefault();
        filter_terms = q.$filter.val();
        if (filter_terms) {
          x = _this.decks_by_id.search(filter_terms);
          decks_with_filter_terms = x.toDict("ref");
          _ref = $(".deck");
          _results = [];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            deck = _ref[_i];
            d = $(deck);
            if (deck.dataset["qid"] in decks_with_filter_terms) {
              _results.push(d.show());
            } else {
              _results.push(d.hide());
            }
          }
          return _results;
        } else {
          _ref1 = $(".deck");
          _results1 = [];
          for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
            deck = _ref1[_j];
            _results1.push($(deck).show());
          }
          return _results1;
        }
      };
    })(this));
  }

  return Quizlet;

})();

q.quizlet = new Quizlet;

YUI().use("autocomplete", "autocomplete-highlighters", function(Y) {
  Y.one("body").addClass("yui3-skin-sam");
  return Y.one("#specificKeyword").plug(Y.Plugin.AutoComplete, {
    resultHighlighter: "phraseMatch",
    queryDelimiter: ',',
    resultListLocator: function(response) {
      return response[1] || [];
    },
    source: "https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=10&namespace=0&format=json&callback={callback}"
  });
});

YUI().use("autocomplete", "autocomplete-filters", "autocomplete-highlighters", function(Y) {
  return Y.one("#filter").plug(Y.Plugin.AutoComplete, {
    resultHighlighter: "phraseMatch",
    resultFilters: 'phraseMatch',
    queryDelimiter: ',',
    source: q.quizlet.decks_by_id.corpusTokens.elements
  });
});
