#!/usr/bin/python
from wsgiref.handlers import CGIHandler
import app

CGIHandler().run(app)
