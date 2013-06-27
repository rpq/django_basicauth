from django.utils import unittest
from django.test.client import Client

TESTSERVER_HOST = 'testserver'
TESTSERVER_ROOT_URL = 'http://{0}'.format(TESTSERVER_HOST)

class LoginTest(unittest.TestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_login_page_redirect(self):
        REDIRECT_URLS = ['/login-redirect', '/login',]
        r = self.client.get('/', follow=True)

        self.assertIn(TESTSERVER_ROOT_URL + REDIRECT_URLS[0],
            dict(r.redirect_chain).keys())
        self.assertIn(TESTSERVER_ROOT_URL + REDIRECT_URLS[1],
            dict(r.redirect_chain).keys())
        self.assertEqual(r.status_code, 200)

    def test_login_page_status_code(self):
        r = self.client.get('/login')
        self.assertEqual(r.status_code, 200)
