from flask import Flask, jsonify
from src.Controller.App.Blueprints.thumbanil_pb import thumb_bp

"""
    A factory function that returns an app app instance
"""


def create_app(debug=False):
    app = Flask(__name__)
    app.config['FLASK_DEBUG'] = debug
    app.register_blueprint(thumb_bp, url_prefix='/thumbnail')

    @app.errorhandler(404)
    def handle_requested_url_not_found(e):
        response = thumb_bp.error_responses.getResponse(404)
        return jsonify(response), 404

    return app
