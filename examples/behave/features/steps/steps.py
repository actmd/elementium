from behave import given, then, when
from selenium.webdriver.common.keys import Keys


@given('we can access the Google page')
def step_impl(context):
    context.elements.navigate("http://www.google.com")


@when('we enter something in the search box')
def step_impl(context):
    # Find the search box
    search_box = context.elements.find('#lst-ib')[0]

    # Enter something into the field to so that we can search for it
    search_box.write("github elementium").write(Keys.RETURN)


@then('we see search results')
def step_impl(context):
    # In a real test, do some assertion here, but since we are lazy, we're
    # just going to quit
    context.elements.browser.quit()
