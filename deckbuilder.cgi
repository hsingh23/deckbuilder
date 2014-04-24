#!/home/deckbuilder/deckbuilder/bin/python

activate_this = '/home/deckbuilder/deckbuilder/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from wsgiref.handlers import CGIHandler
import server

CGIHandler().run(server)
