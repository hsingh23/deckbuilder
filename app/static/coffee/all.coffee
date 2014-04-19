$.q = {}
q = $.q

class Quizlet
	baseUrl: "https://api.quizlet.com/2.0"
	key: "client_id=2xvUtAyRyn"
	decks: {}
	$decks: $("#decks")
	collectedIds: []
	constructor: () ->
		@template = Handlebars.compile($("#deckTemplate").html())
		@populate = (decks) ->
			deckContext =
				decks: decks
			@$decks.append @template deckContext
		@searchSetsUrl = "#{@baseUrl}/search/sets?#{@key}"
		@setsUrl= "#{@baseUrl}/sets?#{@key}"
		@getCardsFromSets = (ids, success) =>
			$.getJSON "#{@setsUrl}&set_ids=#{ids.join()}&callback=?", (data) =>
				for deck in data
					@decks[deck.id] = deck
				@populate(data)

		@getSets = (term, conditions) ->
			$.getJSON "#{@searchSetsUrl}&q=#{term.trim()}&per_page=50&page=1&callback=?"
			, (data) => 
				ids = (deck.id for deck in data.sets)
				uids = _.difference(ids, @collectedIds)
				@collectedIds = _.union @collectedIds, ids
				@decks[term] = 
					term: term
					# may not need - denormalized for searching
					result: data
					ids: ids
					conditions: conditions
				@getCardsFromSets uids

		$("#getDecks").submit (e) => 
			@$decks.empty()
			for x in $("#specificKeyword").val().split(",")
				@getSets x 
			e.preventDefault()

		q.mousedown = (e) ->
			q.md = true
			q.mouseover(e)

		q.mouseover = (e) ->
			if q.md
				debugger
				$(this).toggleClass("selected")


		$("#decks").on "click", ".card", (e) ->
			$(this).toggleClass("selected")
		.on "mouseover", ".card", (e) ->
			$.md = 
		.on "mousedown", q.mousedown
		# .on "mouseup", (e) ->
		# 	$.md = false

q.quizlet = new Quizlet
	