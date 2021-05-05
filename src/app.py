"""Flask Application"""

# load libaries
from flask import Flask, jsonify

# load modules
from src.endpoints.tweet import tweet
from src.endpoints.swagger import swagger_ui_blueprint, SWAGGER_URL

from src.sqlite import db
import os

# init Flask app
app = Flask(__name__)
app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), "sqlite", "tweets.db")

# init database
db.init_app(app)

# register blueprints. ensure that all paths are versioned!
app.register_blueprint(tweet, url_prefix="/api/v1/tweet")

from src.api_spec import spec
# register all swagger documented functions here

with app.test_request_context():
    for fn_name in app.view_functions:
        if fn_name == 'static':
            continue
        print(f"Loading swagger docs for function: {fn_name}")
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)


@app.route("/api/swagger.json")
def create_swagger_spec():
    """
    Swagger API definition.
    """
    return jsonify(spec.to_dict())


app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
