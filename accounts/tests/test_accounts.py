from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from ..models import User


class UserTests(APITestCase):
    def test_register_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('register')
        data = {'username': 'username1', 'password': 'qwerty'}
        response = self.client.post(url, data, format='json')
        # check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertTrue('token' in response.data)
        # check user created
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'username1')
        expected_user = User.objects.get(username='username1')
        # check token for user created
        self.assertEqual(Token.objects.count(), 1)
        expected_token = Token.objects.get(user=expected_user)
        self.assertEqual(expected_token.key, response.data['token'])
    
    def test_register_error(self):
        url = reverse('register')
        # check max length error
        data = {'username': 'too long username 123123123123123123123123',
                'password': 'qwerty'}
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
