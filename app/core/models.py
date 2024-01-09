from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
	BaseUserManager, PermissionsMixin

from django.conf import settings


class UserManager(BaseUserManager):
	"""Кастомный менеджер для модели юзера"""

	def create_user(self, email, password=None, **extra_fields):
		"""Метод для создания обычного пользователя."""

		if not email:
			raise ValueError('Mail-является обязательным для заполнения.')
		user = self.model(email=self.normalize_email(email), **extra_fields)
		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, email, password):
		"""Метод лдля создания пользователя с суперправами"""

		user = self.create_user(email=email, password=password)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)

		return user


class User(AbstractBaseUser, PermissionsMixin):
	"""Custom User Model."""
	email = models.EmailField(max_length=255, unique=True)
	name = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'


class Recipe(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	time_minutes = models.IntegerField()
	price = models.DecimalField(max_digits=6, decimal_places=2)
	link = models.CharField(max_length=255, blank=True)

	def __str__(self):
		return self.title
