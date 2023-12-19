"""
Тесты ждля моделей Django.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
	"""User model Test"""

	def test_create_user_with_email_successful(self):
		email = 'qwe@example.com'
		password = 'qweewq123321'
		user = User.objects.create_user(
			email=email,
			password=password
		)

		self.assertEquals(user.email, email)
		self.assertTrue(user.check_password(password))

	def test_new_user_email_normalized(self):
		sample = (
			('qwe1@EXAMPLE.com', 'qwe1@example.com'),
			('Qwe2@Example.com', 'Qwe2@example.com'),
			('QWE3@EXAMPLE.COM', 'QWE3@example.com'),
			('qwe4@example.COM', 'qwe4@example.com'),
		)
		for email, expected in sample:
			user = get_user_model().objects.create_user(
				email, password='qweewq12331'
			)
			self.assertEqual(user.email, expected)

	def test_user_without_email_error(self):
		with self.assertRaises(ValueError):
			get_user_model().objects.create_user(
				email='',
				password='qweewq123321'
			)

	def test_create_superuser(self):
		user = get_user_model().objects.create_superuser(
			email='qwe@example.com',
			password='qweewq123321'
		)
		self.assertTrue(user.is_superuser)
		self.assertTrue(user.is_staff)
