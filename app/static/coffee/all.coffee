String::strip = -> if String::trim? then @trim() else @replace /^\s+|\s+$/g, ""
String::lstrip = -> @replace /^\s+/g, ""
String::rstrip = -> @replace /\s+$/g, ""
Array::toDict = (key) ->
  @reduce ((dict, obj) -> dict[ obj[key] ] = obj if obj[key]?; return dict), {}

$.q = 
	$decks: $("#decks")
	$filter: $("#filter")
q = $.q

class Quizlet
	baseUrl: "https://api.quizlet.com/2.0"
	key: "client_id=2xvUtAyRyn"
	decks: {}
	decks_by_id: lunr () ->
		@field "terms"
		@field "definitions"
		@field "title"
		@field "description"
		@ref "id"

	collectedIds: []
	constructor: () ->
		@template = Handlebars.compile($("#deckTemplate").html())
		@show_only = (ids) ->
			for deck in $(".deck")
				debugger
			#for deck in @hidden_decks:
		@populate = (decks) ->
			deckContext =
				decks: decks
			q.$decks.append @template deckContext
		@searchSetsUrl = "#{@baseUrl}/search/sets?#{@key}"
		@setsUrl= "#{@baseUrl}/sets?#{@key}"
		@getCardsFromSets = (ids, success) =>
			$.getJSON "#{@setsUrl}&set_ids=#{ids.join()}&callback=?", (data) =>
				for deck in data
					@decks[deck.id] = data
					@add_to_lunr(deck)
				@populate(data)

		@getSets = (term) ->
			$.getJSON "/decks/#{term}", (data) =>
				ids = (deck.id for deck in data.sets)
				uids = _.difference(ids, @collectedIds)
				@collectedIds = _.union @collectedIds, ids
				@decks[term] = 
					term: term
					result: data
					ids: ids
				@getCardsFromSets uids
				
		@add_to_lunr = (deck) ->
			formated_deck = 
				terms: (term for term in deck.terms).join(' ')
				definitions: (term for term in deck.terms).join(' ')
				title: deck.title
				description: deck.description
				id: deck.id
			@decks_by_id.add formated_deck

		$("#getDecks").submit (e) => 
			@terms = (x.trim() for x in $("#specificKeyword").val().split(","))
			for x in @terms
				@getSets x 
			e.preventDefault()

			
		q.mousedown = (e) ->
			e.preventDefault()
			q.md = true
			q.selected = $(this).hasClass("selected")
			q.mouseover(e)

		q.mouseover = (e) ->
			e.preventDefault()
			if q.md is true and q.selected is $(this).hasClass("selected")
				$(this).toggleClass("selected")

		q.mouseup = (e) ->
			e.preventDefault()
			q.md = false

		q.mouseleave = (e) ->
			q.md = false
			q.selected = false


		q.$decks.on "click", ".card", (e) ->
			$(this).toggleClass("selected")
		.on "mouseover", ".card", q.mouseover
		.on "mousedown", ".card", q.mousedown
		.on "mouseup", ".card", q.mouseup
		.on "mouseleave", ".deck", q.mouseleave

		$("#reset").on "click", (e) ->
			e.preventDefault()
			q.$decks.empty()

		$("#filterDecks").submit (e)=>
			e.preventDefault()
			filter_terms = q.$filter.val()
			x = @decks_by_id.search(filter_terms)
			decks_with_filter_terms = x.toDict("ref")
			@show_only(decks_with_filter_terms)

q.quizlet = new Quizlet

YUI().use "autocomplete", "autocomplete-highlighters", (Y) ->
	Y.one("body").addClass "yui3-skin-sam"
	Y.one("#specificKeyword").plug Y.Plugin.AutoComplete,
		resultHighlighter: "phraseMatch"
		queryDelimiter: ','
		resultListLocator: (response) ->
			(response[1]) or []
		source: "https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=10&namespace=0&format=json&callback={callback}"

YUI().use "autocomplete", "autocomplete-filters", "autocomplete-highlighters", (Y) ->
	Y.one("#filter").plug Y.Plugin.AutoComplete,
		resultHighlighter: "phraseMatch"
		resultFilters: 'phraseMatch'
		queryDelimiter: ','
		source: q.quizlet.decks_by_id.corpusTokens.elements