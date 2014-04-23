var Quizlet, q;

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
    this.field("terms", 300);
    this.field("definitions", 300);
    this.field("title", 50);
    this.field("description", 50);
    return this.ref("id");
  });

  Quizlet.prototype.collectedIds = [];

  function Quizlet() {
    this.template = Handlebars.compile($("#deckTemplate").html());
    this.show_ids = function(ids) {
      return this.hidden_decks = $(".deck").detach();
    };
    this.populate = function(decks) {
      var deckContext;
      deckContext = {
        decks: decks
      };
      return q.$decks.append(this.template(deckContext));
    };
    this.searchSetsUrl = "" + this.baseUrl + "/search/sets?" + this.key;
    this.setsUrl = "" + this.baseUrl + "/sets?" + this.key;
    this.getCardsFromSets = (function(_this) {
      return function(ids, success) {
        return $.getJSON("" + _this.setsUrl + "&set_ids=" + (ids.join()) + "&callback=?", function(data) {
          var deck, _i, _len;
          for (_i = 0, _len = data.length; _i < _len; _i++) {
            deck = data[_i];
            _this.decks[deck.id] = data;
            _this.add_to_lunr(deck);
          }
          return _this.populate(data);
        });
      };
    })(this);
    this.getSets = function(term, conditions) {
      return $.getJSON("" + this.searchSetsUrl + "&q=" + (term.trim()) + "&per_page=50&page=1&callback=?", (function(_this) {
        return function(data) {
          var deck, ids, uids;
          ids = (function() {
            var _i, _len, _ref, _results;
            _ref = data.sets;
            _results = [];
            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
              deck = _ref[_i];
              _results.push(deck.id);
            }
            return _results;
          })();
          uids = _.difference(ids, _this.collectedIds);
          _this.collectedIds = _.union(_this.collectedIds, ids);
          _this.decks[term] = {
            term: term,
            result: data,
            ids: ids,
            conditions: conditions
          };
          return _this.getCardsFromSets(uids);
        };
      })(this));
    };
    this.add_to_lunr = function(deck) {
      var formated_deck, term;
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
            term = _ref[_i];
            _results.push(term);
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
          _this.getSets(x);
        }
        return e.preventDefault();
      };
    })(this));
    q.selectCard = function($this) {};
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
    $("#filterDecks").submit((function(_this) {
      return function(e) {
        var decks_with_filter_terms, filter_terms, x;
        e.preventDefault();
        filter_terms = q.$filter.val();
        x = _this.decks_by_id.search(filter_terms);
        decks_with_filter_terms = x.toDict("ref");
        return _this.show_ids;
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
