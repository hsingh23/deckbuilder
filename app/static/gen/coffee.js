var Quizlet, q;

Quizlet = (function() {
  Quizlet.prototype.mousedown = function(e) {
    this.md = true;
    return this.mouseover(e);
  };

  Quizlet.prototype.mouseover = function(e) {
    if (this.md) {
      return $(this).toggleClass("selected");
    }
  };

  Quizlet.prototype.baseUrl = "https://api.quizlet.com/2.0";

  Quizlet.prototype.key = "client_id=2xvUtAyRyn";

  Quizlet.prototype.decks = {};

  Quizlet.prototype.$decks = $("#decks");

  Quizlet.prototype.collectedIds = [];

  function Quizlet() {
    var q;
    this.template = Handlebars.compile($("#deckTemplate").html());
    this.populate = function(decks) {
      var deckContext;
      deckContext = {
        decks: decks
      };
      return this.$decks.append(this.template(deckContext));
    };
    this.searchSetsUrl = "" + this.baseUrl + "/search/sets?" + this.key;
    this.setsUrl = "" + this.baseUrl + "/sets?" + this.key;
    this.getCardsFromSets = (function(_this) {
      return function(ids, success) {
        return $.getJSON("" + _this.setsUrl + "&set_ids=" + (ids.join()) + "&callback=?", function(data) {
          var deck, _i, _len;
          for (_i = 0, _len = data.length; _i < _len; _i++) {
            deck = data[_i];
            _this.decks[deck.id] = deck;
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
    $("#getDecks").submit((function(_this) {
      return function(e) {
        var x, _i, _len, _ref;
        _this.$decks.empty();
        _ref = $("#specificKeyword").val().split(",");
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          x = _ref[_i];
          _this.getSets(x);
        }
        return e.preventDefault();
      };
    })(this));
    q = this;
    $("#decks").on("click", ".card", function(e) {
      return $(this).toggleClass("selected");
    }).on("mouseover", ".card", q.mouseover).on("mousedown", q.mousedown);
  }

  return Quizlet;

})();

q = new Quizlet;
