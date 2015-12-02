"""Behave environment file for behave-elementium example"""

from selenium import webdriver

from elementium.drivers.se import SeElements


def before_all(context):
    # Create an Elements object that wraps the Selenium Firefox driver
    # Note: You could also setup this elements outside of the behave context
    # and just import it in your modules instead of explicitly associating it
    # with the Behave context.
    context.elements = SeElements(webdriver.Firefox())


def before_scenario(context, scenario):
    # For fun, let's make sure we set the window size for consistency
    context.elements.set_window_size(800, 600)
