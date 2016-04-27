import time
from pytest_bdd import given


@given('I am logged in via facebook')
def facebook_login(transactional_db, browser, facebook_user, live_server):
    browser.visit('index')
    browser.is_element_present_by_id('login')
    browser.find_by_id('login').click()
    browser.fill_form(facebook_user)
    browser.find_by_id('loginbutton').click()
    time.sleep(1)
    browser.find_by_tag('body').click()
    time.sleep(1)
    browser.find_by_css('button[name=__CONFIRM__]').click()
    assert browser.is_at('index')
