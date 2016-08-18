"""Simple example to user Elementium to wrap around the Selenium driver

This sets up a driver, and uses Elementium to do some basic work.

NOTE:
    1) If Google ever changes their main page, this example will break.
    2) This assumes that you have Firefox installed on your machine
    3) This was tested on an OS X 10.10 machine running Firefox. YMMV.

To run:

    pip install -U selenium
    python simple.py
"""

from __future__ import absolute_import
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from elementium.drivers.se import SeElements

# Create an Elements object that wraps the Selenium Firefox driver
elements = SeElements(webdriver.Firefox())

# Navigate to the Google search page
elements.navigate("http://www.google.com")

# Find the search box
search_box = elements.find('#lst-ib')[0]

# Enter something into the field to so that we can search for it
search_box.write("github elementium").write(Keys.RETURN)

# Quite the browser
elements.browser.quit()
