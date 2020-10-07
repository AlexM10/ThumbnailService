from src.Controller.App.app_factory import create_app

"""
    A main point entry to the server
"""
if __name__ == '__main__':
    create_app().run(debug=False)
