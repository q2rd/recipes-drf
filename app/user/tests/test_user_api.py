"""
тесты для эндпоинтов юзеров
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
	return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
	def setUp(self) -> None:
		self.client = APIClient()

	def test_create_user_success(self):
		payload = {
			'email': 'test@example.com',
			'password': 'qweewq123321',
			'name': 'test_user'
		}
		response = self.client.post(CREATE_USER, payload)
		self.assertEquals(response.status_code, status.HTTP_201_CREATED)
		user = get_user_model().objects.get(email=payload.get('email'))
		self.assertTrue(user.check_password(payload.get('password')))
		self.assertNotIn('password', response.data)

	def test_user_with_taken_email(self):
		payload = {
			'email': 'test@example.com',
			'password': 'qweewq123321',
			'name': 'test_user'
		}
		create_user(**payload)
		response = self.client.post(CREATE_USER, payload)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_short_password_error(self):
		payload = {
			'email': 'test@example.com',
			'password': 'qwe',
			'name': 'test_user'
		}
		response = self.client.post(CREATE_USER, payload)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
		user_in_db = get_user_model().objects.filter(
			email=payload.get('email')).exists()
		self.assertFalse(user_in_db)

	def test_create_token_for_user(self):
		user_details = {
			'name': 'Test Name',
			'email': 'test@example.com',
			'password': 'test-user-password123',
		}
		create_user(**user_details)

		payload = {
			'email': user_details['email'],
			'password': user_details['password'],
		}
		res = self.client.post(TOKEN_URL, payload)

		self.assertIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_200_OK)

	def test_create_toke_with_invalid_creds(self):
		create_user(email='qwe@example.com', password='qwe123321')
		payload = {'email': 'qwe@example.com', 'password': 'pass'}
		response = self.client.post(TOKEN_URL, payload)
		self.assertNotIn('token', response.data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_blank_password_field(self):
		payload = {'email': 'qwe@example.com', 'password': ''}
		response = self.client.post(TOKEN_URL, payload)

		self.assertNotIn('token', response.data)
		self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_unauthorized_user(self):
		response = self.client.get(ME_URL)

		self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):

	def setUp(self) -> None:
		self.user = create_user(
			email='qwe@example.com',
			password='qwe123321',
			name='Qwe ewq'
		)
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)

	def test_auth_user_get_self_profile_success(self):
		response = self.client.get(ME_URL)

		self.assertEquals(response.status_code, status.HTTP_200_OK)
		self.assertEquals(
			response.data,
			{
				'name': self.user.name,
				'email': self.user.email
			}
		)

	def test_post_not_allowed_for_me_endpoint(self):
		response = self.client.post(ME_URL, {})

		self.assertEquals(response.status_code,
						  status.HTTP_405_METHOD_NOT_ALLOWED)

	def test_update_user_profile(self):
		payload = {'name': 'New qwe', 'password': '123321qweewq'}

		response = self.client.patch(ME_URL, payload)

		self.user.refresh_from_db(fields=('name', 'password'))

		self.assertEquals(self.user.name, payload.get('name'))
		self.assertTrue(self.user.check_password(payload['password']))
		self.assertEquals(response.status_code, status.HTTP_200_OK)
