from typing import Dict

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from ..models import Account


class RegisterTests(APITestCase):
    register_url = 'accounts-register'
    
    def test_register(self):
        """
        Ensure we can create a new account object.
        """
        data = {'username': 'username1', 'password': 'qwerty'}
        url = reverse(self.register_url)
        response = self.client.post(url, data, format='json')
        # check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertTrue('token' in response.data)
        # check user created
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().username, 'username1')
        expected_user = Account.objects.get(username='username1')
        # check token for user created
        self.assertEqual(Token.objects.count(), 1)
        expected_token = Token.objects.get(user=expected_user)
        self.assertEqual(expected_token.key, response.data['token'])
    
    def test_register_error(self):
        # check max length error
        data = {'username': 'too long username 123123123123123123123123',
                'password': 'qwerty'}
        url = reverse(self.register_url)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # todo add error text check
        # check creation error
        data = {'username': 'username', 'password': 'qwerty'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertTrue(response.data['errors'], {'general': 'User already exists'})


class LoginTests(APITestCase):
    data = {'username': 'username1', 'password': 'qwerty'}
    register_url = 'accounts-register'
    login_url = 'accounts-login'
    
    def setUp(self) -> None:
        url = reverse(self.register_url)
        self.client.post(url, self.data, format='json')
    
    def test_login(self):
        url = reverse(self.login_url)
        response = self.client.post(url, self.data, format='json')
        actual_token = response.data['token']
        account = Account.objects.get(username=self.data['username'])
        expected_token = Token.objects.get(user=account).key
        self.assertTrue(response.data['success'])
        self.assertEqual(actual_token, expected_token)
    
    # todo add error login tests
