from django.test import TestCase
from django.test import Client


# Create your tests here.


class IndexViewTests(TestCase):
    def setUp(self):
        # Creating a client for testing
        self.client = Client()

    def test_index_view(self):
        response = self.client.get('/')
        # Check, if index page is loading
        # and there are no cookies before authorization
        # and registration form goes to browser in response
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('mybook_authorization_cookie', self.client.cookies)
        self.assertIn('form', response.context)


class LoginViewTests(TestCase):
    def setUp(self):
        # Creating a client for testing
        self.client = Client()

    def test_login_view_post_failpr(self):
        # Check if login view does not redirects to main page with POST request
        # and incorrect auth credentials and not retrieves auth cookies
        response = self.client.post(
            '/login/',
            {'e_mail': 'smthingrandomemail123@gmail.com', 'password': '12RanD0mPassW4d'},
            follow=True
        )
        self.assertEqual([], response.redirect_chain)
        self.assertNotIn('mybook_authorization_cookie', self.client.cookies)

    def test_login_view_post_success(self):
        # Check if login view redirects to main page with POST request
        # and correct auth credentials and also retrieves auth cookies
        # and returns books list for user
        response = self.client.post(
            '/login/',
            {'e_mail': 'randomtestemail112233@gmail.com', 'password': 'ptp2019ptp'},
            follow=True
        )
        self.assertEqual([('/', 302)], response.redirect_chain)
        self.assertIn('mybook_authorization_cookie', self.client.cookies)
        self.assertIn('books', response.context)

    def test_login_view_get(self):
        # Check if login view redirects to main page with GET request
        response = self.client.get(
            '/login/',
            follow=True
        )
        self.assertEqual([('/', 302)], response.redirect_chain)


class LogoutViewTests(TestCase):
    def setUp(self):
        # Creating a client for testing
        self.client = Client()

    def test_logout_view(self):
        response = self.client.get('/logout/', follow=True)
        # Check if logout redirects to main page
        # and clears cookies
        self.assertEqual([('/', 302)], response.redirect_chain)
