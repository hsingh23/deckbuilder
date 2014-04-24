from flask import Flask
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
app.config.from_object("__config")

assets = Environment(app)
assets.url = app.static_url_path
coffee = Bundle("coffee/all.coffee", filters="coffeescript", output="gen/coffee.js")
js_dev = Bundle("js/jquery-1.11.0.js", "js/underscore.js", "js/handlebars-v1.3.0.js", "js/bootstrap.js", "js/lunr.js",output="gen/devjs.js")
js = Bundle("js/jquery-1.11.0.min.js", "js/underscore-min.js","js/bootstrap.min.js", "js/handlebars.runtime-v1.3.0.js", "js/lunr.min.js", output="gen/lib.js")
scss = Bundle("scss/all.scss", filters="scss", output="gen/main.css") 
assets.register('coffee', coffee)
assets.register('js_dev', js_dev)
assets.register('js', js)
assets.register('scss', scss)

from app import views