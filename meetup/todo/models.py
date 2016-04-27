from django.conf import settings
from django.db import models


class Todo(models.Model):

    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {}'.format(self.user, self.name)


class User(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    access_token = models.TextField()
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)

    is_active = True
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    def is_authenticated(self):
        return True

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name).strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.get_full_name()
