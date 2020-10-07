import unittest

from src.Controller.App.app_factory import create_app


class ServerTests(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    """Test if the main page returns error 404"""

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    """Test if the thumbnail page returns OK 200"""

    def test_thumbnail_response200(self):
        request = "http://localhost:5000/thumbnail?url=https://www.willcookforsmiles.com/wp-content/uploads/2018/06/4" \
                  "-Ingredient-Orange-Salmon-4.jpg&width=200&height=200 "
        response = self.app.get(request, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    """Test if the thumbnail page returns error 400 when the url wrong"""

    def test_thumbnail_response400(self):
        request = "http://localhost:5000/thumbnail?url=https://www.willcookforsmiles.com/wp-content/uploads/2018/06/4" \
                  "-Ingredient-Orange-Salmon-4.jpgasdad&width=200&height=200 "
        response = self.app.get(request, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    """Test if the thumbnail page returns error 422 when one parameter or more are less then zero"""

    def test_thumbnail_response4221(self):
        request = "http://localhost:5000/thumbnail?url=https://www.willcookforsmiles.com/wp-content/uploads/2018" \
                  "/06/4-Ingredient-Orange-Salmon-4.jpg&width=200&height=-1 "
        response = self.app.get(request, follow_redirects=True)
        self.assertEqual(response.status_code, 422)

    """Test if the thumbnail page returns error 422 when one parameter is missing"""

    def test_thumbnail_respons4222(self):
        request = "http://localhost:5000/thumbnail?url=https://www.willcookforsmiles.com/wp-content/uploads/2018" \
                  "/06/4-Ingredient-Orange-Salmon-4.jpg&width=200 "
        response = self.app.get(request, follow_redirects=True)
        self.assertEqual(response.status_code, 422)

    """Test if the thumbnail page returns error 422 when there is no url or some unexpected request"""

    def test_thumbnail_respons4223(self):
        request = "http://localhost:5000/thumbnail?width=200&height=200"
        response = self.app.get(request, follow_redirects=True)
        self.assertEqual(response.status_code, 422)
