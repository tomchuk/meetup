from django.conf import settings
from django.contrib.auth import (
  authenticate,
  login as auth_login,
  logout as auth_logout,
)
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
import requests

from .models import Todo
from .serializers import TodoSerializer

FB_OAUTH_URL = 'https://www.facebook.com/dialog/oauth?client_id={}&redirect_uri={}&scope={}'
FB_TOKEN_URL = 'https://graph.facebook.com/v2.6/oauth/access_token'
FB_SCOPE = 'public_profile,email'


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Todo.objects.order_by('-pk')
        else:
            return Todo.objects.filter(user=user).order_by('-pk')


def index(request):
    return render(request, 'index.html')


def _fb_redirect(request):
    return redirect(
      FB_OAUTH_URL.format(
        settings.FB_APP_ID,
        request.build_absolute_uri(),
        FB_SCOPE,
      )
    )


def login(request):

    if request.user.is_authenticated():
        # TODO - logout
        return redirect('index')

    code = request.GET.get('code')
    token = request.GET.get('token')

    if not code and not token:
        return _fb_redirect(request)

    if code:
        resp = requests.get(
          FB_TOKEN_URL,
          params={
            'client_id': settings.FB_APP_ID,
            'redirect_uri': request.build_absolute_uri(),
            'client_secret': settings.FB_APP_SECRET,
            'code': code,
          }
        )
        if resp.status_code != 200:
            return _fb_redirect(request)
        token = resp.json()['access_token']

    user = authenticate(token=token)
    if user is not None:
        user_logged_in.disconnect(update_last_login)
        auth_login(request, user)

    return redirect('index')


def logout(request):
    auth_logout(request)
    return redirect('index')
