"""
Polls application tests.
"""

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth import get_user_model

from polls.views import PollViewSet


class TestPoll(APITestCase):
    """
    Poll's actions tests.
    """

    def setUp(self):
        """
        Set up poll's test.

        Create request and define views and uri.
        Set up user and authentication token.
        """
        self.factory = APIRequestFactory()
        self.view = PollViewSet.as_view({'get': 'list'})
        self.uri = '/polls/'

        # User and token set up.
        self.setup_user()
        self.setup_auth_token()

    def setup_user(self):
        """
        Create a new test user instance.
        """
        self.user = get_user_model().objects.create_user(
            'test', email='testuser@test.com', password='test')

    def setup_auth_token(self):
        """
        Create and link a new authentication token.
        """
        if not self.user:
            raise Exception("First need to call setup_user method.")

        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_list(self):
        """
        List action assertion.
        """
        request = self.factory.get(
            self.uri, HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.view(request)

        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {} instead'
                         .format(response.status_code))
