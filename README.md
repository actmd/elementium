elementium
==========

Elementium: Browser testing done right.

Homepage
--------

Visit the home of `elementium` on the web: [Elementium](http://github.com/actmd/elementium). 

For an intruction to why you'd want to use elementium, take a look at the following [post](http://prschmid.blogspot.com/2014/07/elementium-browser-testing-done-right.html).

Installation
------------

### The easy way

```sh
pip install elementium
```

### The developer way

```sh
git clone git@github.com:actmd/elementium.git
cd elementium
python setup.py install
```

Contributing
------------

If you would like to contribute to this project, you will need to use [git flow](https://github.com/nvie/gitflow). This way, any and all changes happen on the development branch and not on the master branch. As such, after you have git-flow-ified your elementium git repo, create a pull request for your branch, and we'll take it from there.

Usage
-----

Currently, the only driver that is implemented makes use of the python [Selenium bindings](http://selenium-python.readthedocs.org/en/latest/api.html). As such, all of the usage examples make use of the Selenium driver.

Let's get started by wrapping our Selenium browser object with a SeElements (Selenium Elements) object.

```python
from selenium import webdriver
from elementium.drivers.se import SeElements

# Initialize the elements wrapper.
# That's all you have to do to get the benefits of Elementium!
elements = SeElements(webdriver.Firefox())
```

Ok, now that you know how to do that, let's find all elements on the page that have the CSS class `ctr-p` on the Google search page.

```python
# Go to the Google search page
elements.navigate('http://www.google.com')

# Find elements on a page for a given class
els = elements.find('.ctr-p')
for el in els:
    print el.value()
```

Under the hood, `find()` will return a new `SeElements` object containing a list of all of the items that matched. All items that are returned by getting the individual elements in the container will by of type `SeElements`. E.g.

```python
# Find elements on a page for a given class
els = elements.find('.ctr-p')
for el in els:
    print type(el)
```

If you would rather get the raw object that is returned by the underlying driver (in this case Selenium), just get the items as follows:

```python
# Find elements on a page for a given class
els = elements.find('.ctr-p')
for item in els.items:
    print type(el)
```

Note: there happens to be a helper alias that will give you the first raw item via ``else.item``.

So far, this has been nothing too special, but how about applying a function to each of those elements? For example, let's say we want to click each one.

```python
# Find all "Search" buttons on the page and click each one
# Don't blame me for that ID... that's what is used by the folks at Google...
elements.find('#gbqfba').foreach(lambda e: e.click())
```

Ok, that seems like an annoying thing to have to write that `foreach` each time you want to click many buttons at once (note, when I say "at once" I mean that they will be clicked sequentially, but with one function call).

```python
# Find all "Search" buttons on the page and click each one
# (there happens to be only one...)
elements.find('#gbqfba').click()
```

Of course, just clicking on the "Search" button with nothing to search for is meaningless. Let's first add some thing to search for in the search box.

```python
# Go to the Google search page
elements.navigate('http://www.google.com')

# Write something in the search box
elements.find('#gbqfq').write('elementium')

# Click the search button
elements.find('#gbqfba').click()
```

Ok, that's all well and great, but how is that different from just using Selenium? Fair question. Let's step it up a bit. One of the big issues with Selenium is waiting for pages to load completely and all of the retry logic that may have to be used to have tests that work well. The common solution is to wrap all of your code with something like `with_retry()` functions. For example, a naive, old way of doing something might have been somthing like:

```python
browser = webdriver.Firefox()
els = None
while not els:
    els = browser.find_element_by_id('#gbqfba')
    time.sleep(0.5)
```

Not only is that ugly, but it's a pain to write that each time. Elementium takes care of all of this for you. For example, we can do something like

```python
# Retry until the search button is on the page before continuing
# This will retry for 20 seconds (by default)
els = elements.find('#gbqfba').until(lambda e: len(e) > 0)

# This will retry for 60 seconds
els = elements.find('#gbqfba').until(lambda e: len(e) > 0, ttl=60)
```

Alternatively, if you know that you want this needs to be on the page before continuing, you can tell the `find()` method to wait.

```python
# Retry until the search button is on the page before continuing
# This will retry for 20 seconds (by default)
els = elements.find('#gbqfba', wait=True)
```

Both of the above methods will raise a ``elementium.elements.TimeoutError`` if the element is not found in the specified period of time. How about if you are running this as part of a test and you want an ``AssertionError`` instead? Simple, just use the `insist()` method instead of the `until()` method. (I.e. `until()` and `insist()` behave the same way, the difference is only in the error they raise if the items are not found.)

```python
# Retry until the search button is on the page before continuing
# This will retry for 20 seconds (by default)
els = elements.find('#gbqfba').insist(lambda e: len(e) > 0)
```

Basically all methods that are part of the `SeElements` object will automatically retried for you. "How does it do all this magic," you ask. I won't go into too much detail here (but feel free to take a look at the code), but under the hood, each selector (e.g. '.foo' or '#foo') is stored as a callback function (similar to something like ``lambda: selenium.find_element_by_id('foo')``). This way, when any of the calls to any of the methods of an element has an expected error (``StaleElementException``, etc.) it will recall this function. If you perform chaining, this will actually propagate that refresh (called ``update()``) up the entire chain to ensure that all parts of the call are valid. Cool!

The Future
----------

There are several features planned for the future to improve Elementium and they will be rolled out as they pass through our internal scrutinty. If you have great ideas, you can be part of Elementium's future as well!

