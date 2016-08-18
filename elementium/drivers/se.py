"""Elemetium elements using the Selenium driver"""

from __future__ import absolute_import

import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select

from elementium.elements import (
    Browser,
    Elements
)
from elementium.util import (
    DEFAULT_SLEEP_TIME,
    DEFAULT_TTL,
    ignored
)
from elementium.waiters import (
    ExceptionRetryWaiter,
    ExceptionRetryElementsWaiter
)

__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"


class WebDriverExceptionRetryWaiter(ExceptionRetryWaiter):

    def __init__(self, n=0, ttl=DEFAULT_TTL):
        """Create a new Waiter

        :param n: The number of times to retry
        :param ttl: The number of seconds to wait.
        """
        super(WebDriverExceptionRetryWaiter, self).__init__(
            WebDriverException, n=n, ttl=ttl)


class WebDriverExceptionRetryElementsWaiter(ExceptionRetryElementsWaiter):

    def __init__(self, elements, n=0, ttl=DEFAULT_TTL):
        """Create a new Waiter

        :param elements: The :class:`Elements` we want to wait on.
        :param n: The number of times to retry
        :param ttl: The number of seconds to wait.
        """
        super(WebDriverExceptionRetryElementsWaiter, self).__init__(
            elements, WebDriverException, n=n, ttl=ttl)


class SeElements(Elements, Browser):
    """Elements making use of the Selenium Web Driver."""

    def __init__(self, browser, context=None, fn=None, config=None, lazy=None):
        """Create a list of elements

        :param browser: The base browser object that we are using.
        :param context: The context that these elements live in. This is the
                        "parent" set of :class:`Elements` that is giving
                        rise to this set of :class:`Elements`.
        :param fn: The function to call to populate the list of browser
                   elements this list of :class:`Elements` refers to.
        :param config: Optional other configuration details in a dictionary.
                       Valid options are:

                        `ttl`: The minimum number of seconds to keep retrying.
                               Each of the methods that supports retrying will
                               also have it's own `ttl`, that can be set, but
                               this will be the default. The default is 20
                               seconds.
                        `lazy`: Whether or not to lazy load the items.

        :param lazy: Whether or not to lazy load the items. If this is ``True``
                     then the :attr:`fn` is evaluated on first access.
                     If, ``False``, then :attr:`fn` is evaluated right away
                     by a call to the update() method. This lazy parameter
                     can also be set in the config dict. Note, that whatever
                     is passed here will OVERWRITE what may be in the config
                     object. Note, by default lazy will be set to ``True``
        """
        super(SeElements, self).\
            __init__(browser, context=context, fn=fn, config=config, lazy=lazy)

    def get(self, i):
        """Get the i-th item as an :class:`Elements` object

        Since the items that we store are the raw web elements returned by the
        driver, this method will wrap them appropriately, to return a 
        :class:`Elements` object.

        :param i: The index of the item to return
        :returns: The item as an :class:`Elements` object
        """
        return SeElements(
            self.browser, context=self, fn=lambda context: [context.items[i]],
            config=self.config)

    def retried(self, fn, update=True, ttl=None):
        """Retry a function for :attr:`ttl` seconds

        :param fn: The function to call
        :param update: Whether or not to call update() on self between each
                       retry.
        :param ttl: The number of seconds to retry.
        :returns: The result of running :attr:`fn`
        """
        ttl = ttl if ttl is not None else self.ttl
        if ttl:
            if update:
                return WebDriverExceptionRetryElementsWaiter(self, ttl=ttl).\
                    wait(fn)
            else:
                return WebDriverExceptionRetryWaiter(ttl=ttl).wait(fn)
        else:
            if update:
                return fn(self)
            else:
                return fn()

    def is_displayed(self, ttl=None):
        """Get whether or not the element is visible

        If there are multiple items in this object, the visibility of the first
        element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``True`` if and only if the first element is visible
        """
        def callback(elements):
            return elements.item.is_displayed() if elements.items else False
        return self.retried(callback, update=True, ttl=ttl)

    def is_enabled(self, ttl=None):
        """Get whether or not the element is enabled

        If there are multiple items in this object, the status of the first
        element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``True`` if and only if the first element is enabled
        """
        def callback(elements):
            return elements.item.is_enabled() if elements.items else False
        return self.retried(callback, update=True, ttl=ttl)

    def is_selected(self, ttl=None):
        """Get whether or not the element is selected

        If there are multiple items in this object, the selected state of the
        first element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``True`` if and only if the first element is select
        """
        def callback(elements):
            return elements.item.is_selected() if elements.items else False
        return self.retried(callback, update=True, ttl=ttl)

    def text(self, ttl=None):
        """Return the text

        If there are multiple items in this object, the text of the first
        element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: The text of the first element
        """
        def callback(elements):
            return elements.item.text if elements.items else None
        return self.retried(callback, update=True, ttl=ttl)

    def tag_name(self, ttl=None):
        """Return the tag name

        If there are multiple items in this object, the tag name of the first
        element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: The tag name of the first element
        """
        def callback(elements):
            return elements.item.tag_name if elements.items else None
        return self.retried(callback, update=True, ttl=ttl)

    def value(self, ttl=None):
        """Get the value

        If there are multiple items in this object, the value of the first
        element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: The value of the first element
        """
        def callback(elements):
            return elements.item.get_attribute('value') \
                   if elements.items else None
        return self.retried(callback, update=True, ttl=ttl)

    def attribute(self, name, ttl=None):
        """Get the attribute with the given name

        If there are multiple items in this object, the attribute of the first
        element will be returned.

        :param name: The name of the attribute
        :param ttl: The minimum number of seconds to keep retrying
        :returns: The attribute of the first element
        """
        def callback(elements):
            return \
                elements.item.get_attribute(name) if elements.items else None
        return self.retried(callback, update=True, ttl=ttl)

    def clear(self, ttl=None):
        """Clear the contents of the elements

        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        """
        return self.foreach(lambda elements: elements.item.clear(), ttl=ttl)

    def click(self, pause=0, ttl=None):
        """Click the element

        If there are multiple elements, each of the elements will be clicked

        :param pause: The number of seconds to pause between clicks if there
                      are multiple things to click
        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        """
        return self.foreach(
            lambda elements: elements.item.click(), pause=pause, ttl=ttl)

    def select(self, i=None, value=None, text=None, ttl=None):
        """Select the element

        If there are multiple elements, each of the elements will be selected.
        At least one of the attributes :attr:`i`, :attr:`value`, or
        :attr:`text` must be supplied

        :param i: The index to select
        :param value: The value to match against
        :param text: The visible text to match against
        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        """
        def callback(elements):
            s = Select(elements.item)
            if i is not None:
                s.select_by_index(i)
            elif value is not None:
                s.select_by_value(value)
            elif text is not None:
                s.select_by_visible_text(text)
            else:
                raise ValueError("i, value, or text must be provided")
        return self.foreach(callback, ttl=ttl)

    def deselect(self, i=None, value=None, text=None, ttl=None):
        """Select the element

        If there are multiple elements, each of the elements will be
        deselected. If :attr:`i`, :attr:`value`, or :attr:`text` are not
        supplied, all values will be deselected.

        :param i: The index to select
        :param value: The value to match against
        :param text: The visible text to match against
        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        """
        def callback(elements):
            s = Select(elements.item)
            if i is not None:
                s.deselect_by_index(i)
            elif value is not None:
                s.deselect_by_value(value)
            elif text is not None:
                s.deselect_by_visible_text(text)
            else:
                s.deselect_all()
        return self.foreach(callback, ttl=ttl)

    def write(self, text, ttl=None):
        """Write text to an element

        Instead of just setting the value of an item, this will "write" the
        text by simulating sending of key press commands.

        :param text: The text to write
        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        """
        return self.foreach(
            lambda elements: elements.item.send_keys(text), ttl=ttl)

    def closest(self, selector, ttl=None):
        """Find the closest element matching the selector.

        :param selector: The selector to use
        :param ttl: The minimum number of seconds to keep retrying
        :returns: The closest element matching the :attr:`selector`
        """
        raise NotImplementedError()

    def parent(self, ttl=None):
        """Get the parent element

        :param ttl: The minimum number of seconds to keep retrying
        :returns: The parent element
        """
        def callback(elements):
            return [elements.item.parent] if elements.items else None
        return SeElements(
            self.browser, context=self, fn=callback, config=self.config)

    def find(self, selector, only_displayed=True, wait=False, ttl=None):
        """Find the elements that match the given selector

        :param selector: The selector to use
        :param only_displayed: Whether or not to only return elements that
                               are displayed
        :param wait: Wait until the selector finds at least 1 element. If this
                     is set to ``True``, the find is retried for the
                     appropriate number of seconds until at least 1 element is
                     found. This is different from just setting the
                     :attr:`ttl`, as it is possible to successfully return
                     from a find with no elements if the DOM is currently
                     changing. Syntactically, setting this to ``True`` is
                     equivalent to::

                        elements.find('selector').until(lambda e: len(e) > 0)

        :param ttl: The minimum number of seconds to keep retrying
        :returns: An :class:`Elements` object containing the web elements that
                  match the :attr:`selector`
        """
        ttl = ttl if ttl is not None else self.ttl
        def callback(elements):
            def inner(e):
                matches = e.item.find_elements_by_css_selector(selector)
                if only_displayed:
                    matches = [obj for obj in matches if obj.is_displayed()]
                return matches
            results = elements.foreach(
                inner,
                return_results=True,
                ttl=ttl)
            return [item for sublist in results for item in sublist]

        elements = SeElements(
            self.browser, context=self, fn=callback, config=self.config)
        if wait:
            return elements.until(lambda e: len(e) > 0, ttl=ttl)
        else:
            return elements

    def find_with_wait(self, selector, only_displayed=True, ttl=None):
        """Find the elements that match the given selector with waiting

        This is equivalent to calling find() with ``wait=True``.

        :param selector: The selector to use
        :param only_displayed: Whether or not to only return elements that
                               are displayed
        :param ttl: The minimum number of seconds to keep retrying
        :returns: An :class:`Elements` object containing the web elements that
                  match the :attr:`selector`
        """
        s = self.find(
            selector, only_displayed=only_displayed, wait=True, ttl=ttl)
        if only_displayed:
            s.insist(lambda e: e.is_displayed())
        else:
            s.insist(lambda e: len(e) > 0)
        return s

    def xpath(self, selector, only_displayed=True, wait=False, ttl=None):
        """Find the elements that match the given xpath selector

        :param selector: The selector to use
        :param only_displayed: Whether or not to only return elements that
                               are displayed
        :param wait: Wait until the selector finds at least 1 element. If this
                     is set to ``True``, the find is retried for the
                     appropriate number of seconds until at least 1 element is
                     found. This is different from just setting the
                     :attr:`ttl`, as it is possible to successfully return from
                     a find with no elements if the DOM is currently changing.
                     Syntactically, setting this to ``True`` is equivalent to::

                        elements.xpath('selector').until(lambda e: len(e) > 0)

        :param ttl: The minimum number of seconds to keep retrying
        :returns: An :class:`Elements` object containing the web elements that
                  match the :attr:`selector`
        """
        ttl = ttl if ttl is not None else self.ttl
        def callback(elements):
            def inner(e):
                matches = e.item.find_elements_by_xpath(selector)
                if only_displayed:
                    matches = [obj for obj in matches if obj.is_displayed()]
                return matches
            results = elements.foreach(
                inner,
                return_results=True,
                ttl=ttl)
            return [item for sublist in results for item in sublist]

        elements = SeElements(
            self.browser, context=self, fn=callback, config=self.config)
        if wait:
            return elements.until(lambda e: len(e) > 0, ttl=ttl)
        else:
            return elements

    def find_link(
            self, selector, exact=True, only_displayed=True, wait=False,
            ttl=None):
        """Find the link elements that match the given selector

        :param selector: The selector to use
        :param exact: Whether or not the link text should be matched exactly
        :param only_displayed: Whether or not to only return elements that
                               are displayed
        :param wait: Wait until the selector finds at least 1 element. If this
                     is set to ``True``, the find is retried for the
                     appropriate number of seconds until at least 1 element is
                     found. This is different from just setting the
                     :attr:`ttl`, as it is possible to successfully return from
                     a find with no elements if the DOM is currently changing.
                     Syntactically, setting this to ``True`` is equivalent to::

                        elements.
                            find_link('selector').
                            until(lambda e: len(e) > 0)

        :param ttl: The minimum number of seconds to keep retrying
        :returns: An :class:`Elements` object containing the web elements that
                  match the :attr:`selector`
        """
        ttl = ttl if ttl is not None else self.ttl
        if exact:
            def callback(elements):
                def inner(e):
                    matches = e.item.find_elements_by_link_text(selector)
                    if only_displayed:
                        matches =\
                            [obj for obj in matches if obj.is_displayed()]
                    return matches
                results = elements.foreach(
                    inner,
                    return_results=True,
                    ttl=ttl)
                return [item for sublist in results for item in sublist]
        else:
            def callback(elements):
                def inner(e):
                    matches =\
                        e.item.find_elements_by_partial_link_text(selector)
                    if only_displayed:
                        matches =\
                            [obj for obj in matches if obj.is_displayed()]
                    return matches
                results = elements.foreach(
                    inner,
                    return_results=True,
                    ttl=ttl)
                return [item for sublist in results for item in sublist]
        
        elements = SeElements(
            self.browser, context=self, fn=callback, config=self.config)
        if wait:
            return elements.until(lambda e: len(e) > 0, ttl=ttl)
        else:
            return elements

    def filter(self, fn):
        """Filter the elements and return only the ones that match the filter

        :param fn: The filter function
        :returns: A new SeElements object with the filter applied
        """
        def callback(elements):
            return [e.item for e in list(filter(fn, elements))]
        return SeElements(
            self.browser, context=self, fn=callback, config=self.config)

    def title(self, ttl=None):
        """Get the title of the page

        :param ttl: The minimum number of seconds to keep retrying
        :returns: The title of the page
        """
        def callback(elements):
            return elements.browser.title
        return self.retried(callback, update=True, ttl=ttl)

    def source(self, ttl=None):
        """Get the source of the page

        :param ttl: The minimum number of seconds to keep retrying
        :returns: The source of the page
        """
        def callback(elements):
            return elements.browser.page_source
        return self.retried(callback, update=True, ttl=ttl)

    def navigate(self, url, ttl=None):
        """Navigate the browser to the given URL

        :param url: The URL to navigate the browser to
        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        """
        self.retried(lambda: self.browser.get(url), update=False)
        return self

    def refresh(self):
        """Refresh the current page

        :returns: ``self``
        """
        self.browser.refresh()
        return self

    def current_url(self):
        """Get the current URL

        :returns: The current URL the browser is displaying
        """
        return self.browser.current_url

    def execute_script(self, script, callback=None, async=False, ttl=None):
        """Execute arbitrary JavaScript

        :param script: The JavaScript to execute
        :param callback: A function to execute with the results of the script.
                         This function should take a single parameter, the
                         results from the script.
        :param async: Whether or not to do it asyncronously
        :param ttl: The minimum number of seconds to keep retrying
        :returns: If :attr:`callback` is provided, then this will return the
                  results form the callback. If not, this will return the
                  results from the script that was executed
        """
        if async:
            raise NotImplementedError(
                "Can't perform async scripts yet. Sorry.")
        results = self.retried(
            lambda: self.browser.execute_script(script), update=False)
        if not callback:
            return results
        else:
            return callback(results)

    def get_window_size(self):
        """Get the size of the browser window

        :returns: A tuple of the form ``(width, height)`` where the units are
                  pixels
        """
        with ignored(Exception):
            dim = self.browser.get_window_size()
            return (dim['width'], dim['height'])
            
    def set_window_size(self, width, height, sleep=DEFAULT_SLEEP_TIME):
        """Set the size of the browser window

        :param width: Browser width in pixels
        :param height: Browser height in pixels
        :param sleep: The number of seconds to sleep after the command to make
                      sure the command has been run
        :returns: ``self``
        """
        with ignored(Exception):
            self.browser.set_window_size(width, height)
            if sleep:
                time.sleep(sleep)
        return self

    def scroll(self, x=0, y=0, sleep=DEFAULT_SLEEP_TIME):
        """Scroll to the given position on the page

        :param x: The x position on the page. This can either be a number
                  (pixels from the left) or a javascript string that evaluates
                  to a position (e.g. ``document.body.scrollWidth``)
        :param y: The y position on the page. This can either be a number
                  (pixels from the top) or a javascript string that evaluates
                  to a position (e.g. ``document.body.scrollHeight``)
        :param sleep: The number of seconds to sleep after the command to make
                      sure the command has been run
        :returns: ``self``
        """
        self.browser.execute_script("window.scrollTo({}, {});".format(x, y))
        if sleep:
            time.sleep(sleep)
        return self

    def scroll_top(self, x=0, sleep=DEFAULT_SLEEP_TIME):
        """Scroll to the top of the page

        :param x: The x position on the page. This can either be a number
                  (pixels from the left) or a javascript string that evaluates
                  to a position (e.g. ``document.body.scrollHeight``)
        :param sleep: The number of seconds to sleep after the command to make
                      sure the command has been run
        :returns: ``self``
        """
        return self.scroll(x=x, y=0, sleep=sleep)

    def scroll_bottom(self, x=0, sleep=DEFAULT_SLEEP_TIME):
        """Scroll to the bottom of the page

        :param x: The x position on the page. This can either be a number
                  (pixels from the left) or a javascript string that evaluates
                  to a position (e.g. ``document.body.scrollHeight``)
        :param sleep: The number of seconds to sleep after the command to make
                      sure the command has been run
        :returns: ``self``
        """
        return self.scroll(x=x, y="document.body.scrollHeight", sleep=sleep)

    def run(self, fn, ttl=None):
        """Run the given function

        :param fn: The function to run
        :param ttl: The minimum number of seconds to keep retrying
        """
        return self.retried(lambda e: fn, update=False, ttl=ttl)

    def switch_to_active_element(self):
        """Get the active element

        :returns: The active element
        """
        def callback(elements):
            return [elements.item.switch_to_active_element()]\
                    if elements.items else None
        return SeElements(
            self.browser, context=self, fn=callback, config=self.config)
