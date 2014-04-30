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
			debugger
			for deck in $(".deck")
				x = $(deck)
				if deck.attributes["data-qid"] not in ids
					$(deck).hide()
				else
					$(deck).show()


		@getDecks = (term) ->
			if term
				$.getJSON "/decks/#{term}", (data) =>
					x = clone data
					@populate x
					for deck in data
						@add_to_lunr deck.json
				
		@populate = (data) ->
			deckContext =
				decks: data
			q.$decks.append @template deckContext

		@add_to_lunr = (deck) ->
			formated_deck = 
				terms: (term for term in deck.terms).join(' ')
				definitions: (definitions for definitions in deck.terms).join(' ')
				title: deck.title
				description: deck.description
				id: deck.id
			@decks_by_id.add formated_deck

		$("#getDecks").submit (e) => 
			@terms = (x.trim() for x in $("#specificKeyword").val().split(","))
			for x in @terms
				@getDecks x 
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

		q.$decks.on "click", ".removeDeck", (e) ->
			e.currentTarget.parentElement.remove()

		$("#export").click (e)->
			terms = (term.textContent for term in $(".card.selected .term"))
			definitions = (definition.textContent for definition in $(".card.selected .definition"))
			cards = JSON.stringify zip(terms, definitions)
			console.log terms, definitions, cards

		$("#filterDecks").submit (e)=>
			e.preventDefault()
			filter_terms = q.$filter.val()
			if filter_terms
				x = @decks_by_id.search(filter_terms)
				decks_with_filter_terms = x.toDict("ref")
				for deck in $(".deck")
					d = $(deck)

					if deck.dataset["qid"] of decks_with_filter_terms
						d.show()
					else
						d.hide()
			else
				for deck in $(".deck")
					$(deck).show()


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