from flask import Flask
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
app.config.from_object("__config")

assets = Environment(app)
assets.url = app.static_url_path

all_dev_js = Bundle(
    Bundle(
        "js/jquery-1.11.0.js",
        "js/underscore.js",
        "js/handlebars-v1.3.0.js",
        "js/bootstrap.js",
        "js/lunr.js",
    ),
    Bundle(
        "coffee/all.coffee",
        filters="coffeescript",
        output="gen/coffee.js"
    ),
    output='gen/dev.js'
)

all_js = Bundle(
    Bundle(
        "js/jquery-1.11.0.min.js",
        "js/underscore-min.js",
        "js/bootstrap.min.js",
        "js/handlebars.runtime-v1.3.0.js",
        "js/lunr.min.js",
    ),
    Bundle(
        "coffee/all.coffee",
        filters="coffeescript",
        output="gen/coffee.js"
    ),
    filters='jsmin',
    output="gen/packed.js"
)
scss = Bundle("scss/all.scss", filters="scss", output="gen/main.css")
assets.register('all_dev_js', all_dev_js)
assets.register('all_js', all_js)
assets.register('scss', scss)

from app import views

if __name__ == "__main__":
    app.run(debug=True)
