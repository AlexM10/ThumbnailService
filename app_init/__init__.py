from src.Controller.App.app_factory import create_app
from flask import Flask, jsonify
from src.Controller.App.Blueprints.thumbanil_pb import thumb_bp
from src.Controller.App.app_factory import create_app

"""
    A main point entry to the server
"""
app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
