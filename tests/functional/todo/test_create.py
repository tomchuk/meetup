from functools import partial

from pytest_bdd import scenario, when, then
from selenium.webdriver.common.keys import Keys

TODO_NAME = 'Buy Milk'
scenario = partial(scenario, 'todo/create-todo.feature')


@scenario('Create a todo')
def test_create_todo():
    pass


@when('I visit the home page')
def visit_home(browser):
    browser.visit('index')
    assert browser.is_at('index')


@when('I fill out the todo name')
def fill_out_todo(browser):
    browser.find_by_css('input.new-todo').fill(TODO_NAME)


@when('I press enter')
def press_enter(browser):
    browser.find_by_css('input.new-todo')._element.send_keys(Keys.ENTER)


@then('I should see my todo')
def should_see_todo(browser):
    assert browser.is_element_present_by_text(TODO_NAME)
