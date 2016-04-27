import os
import time
import requests

from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch

import pytest
from splinter.driver.webdriver import chrome


class WebDriver(chrome.WebDriver):
    django_live_server_url = ''

    def _resolve_url(self, url, *args, **kwargs):
        try:
            url = reverse(url, args=args, kwargs=kwargs)
        except NoReverseMatch:
            pass
        return url

    def visit(self, url, *args, **kwargs):
        url = self._resolve_url(url, *args, **kwargs)
        if not url.startswith('http'):
            url = self.django_live_server_url + url
        super(WebDriver, self).visit(url)

    def is_at(self, url, *args, **kwargs):
        url = self._resolve_url(url, *args, **kwargs)
        for x in range(10):
            browser_url = self.url.rsplit('#')[0].rsplit('?')[0]
            if browser_url.endswith(url):
                return True
            time.sleep(0.5)
        return False


@pytest.fixture
def browser(request, live_server):
    service_args = ['--no-proxy-server', '--noerrdialogs']
    webdriver = WebDriver(wait_time=2, service_args=service_args)
    webdriver.django_live_server_url = str(live_server)
    webdriver.main_window_handle = webdriver.driver.current_window_handle
    webdriver.driver.set_window_size(1280, 1024)

    def fin():
        for window_handle in webdriver.driver.window_handles:
            if window_handle != webdriver.main_window_handle:
                webdriver.driver.switch_to_window(window_handle)
                time.sleep(0.5)
                webdriver.driver.close()
        webdriver.driver.switch_to_window(webdriver.main_window_handle)
        webdriver.driver.close()

    request.addfinalizer(fin)
    return webdriver


@pytest.fixture
def pytestbdd_feature_base_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'features')


@pytest.fixture
def facebook_user(request):
    """
    A test email/pass for logging into the facebook auth dialog
    """
    fb_url = 'https://graph.facebook.com'
    fb_test_user_path = '/{app_id}/accounts/test-users'
    fb_del_user_path = '/{user_id}'
    fb_qs = '?access_token={app_id}|{app_secret}'

    url = (fb_url + fb_test_user_path + fb_qs).format(
      app_id=settings.FB_APP_ID,
      app_secret=settings.FB_APP_SECRET,
    )
    response = requests.post(url)
    user_data = response.json()

    if 'error' in user_data:
        pytest.fail('Facebook API error')

    def fin():
        url = (fb_url + fb_del_user_path + fb_qs).format(
          app_id=settings.FB_APP_ID,
          app_secret=settings.FB_APP_SECRET,
          user_id=user_data['id']
        )
        requests.delete(url)
    request.addfinalizer(fin)

    return {
      'email': user_data['email'],
      'pass': user_data['password']
    }
