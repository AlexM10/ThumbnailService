from src.Controller.App.app_factory import create_app
from flask import Flask, jsonify
from src.Controller.App.Blueprints.thumbanil_pb import thumb_bp

"""
    A main point entry to the server
"""

app = Flask(__name__)
app.config['FLASK_DEBUG'] = True
app.register_blueprint(thumb_bp, url_prefix='/thumbnail')


@app.errorhandler(404)
def handle_requested_url_not_found(e):
    response = thumb_bp.error_responses.getResponse(404)
    return jsonify(response), 404


if __name__ == '__main__':
    create_app().run(debug=False)
