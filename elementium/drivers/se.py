"""Elemetium elements using the Selenium driver"""

__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"


import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select

from elementium.elements import (
    Browser,
    DEFAULT_SLEEP_TIME,
    Elements,
    with_retry,
    with_update
)


class SeElements(Elements, Browser):
    """Elements making use of the Selenium Web Driver."""

    def __init__(self, browser, context=None, fn=None, config=None):
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
        """
        super(SeElements, self).\
            __init__(browser, context=context, fn=fn, config=config)

    def get(self, i):
        """Get the i-th item as an :class:`Elements` object

        Since the items that we store are the raw web elements returned by the
        driver, this method will wrap them appropriately, to return a 
        :class:`Elements` object.

        :param i: The index of the item to return
        :returns: The item as an :class:`Elements` object
        """
        return SeElements(
            self.browser, self, lambda context: [context.items[i]], self.config)

    def with_retry(self, fn, ttl=None):
        """Retry a function for :attr:`ttl` seconds

        :param fn: The function to call
        :param ttl: The minimum number of seconds to keep retrying
        :returns: The result of running :attr:`fn`
        """
        return with_retry(fn, WebDriverException, ttl=ttl if ttl else self.ttl)

    def with_update(self, fn, ttl=None):
        """Retry a function for :attr:`ttl` seconds

        Unlike :func:`with_retry`, this will update() `self` on each
        failure instead of just retrying.

        :param fn: The function to call
        :returns: The result of running :attr:`fn`
        """
        return with_update(
            fn, self, WebDriverException, ttl=ttl if ttl else self.ttl)

    def is_displayed(self, ttl=None):
        """Get whether or not the element is visibile

        If there are multiple items in this object, the visibility of the first
        element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``True`` if and only if the first element is visible
        """
        def callback(elements):
            return elements.item.is_displayed() if elements.items else False
        return self.with_update(callback, ttl=ttl)

    def is_enabled(self, ttl=None):
        """Get whether or not the element is enabled

        If there are multiple items in this object, the status of the first
        element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``True`` if and only if the first element is enabled
        """
        def callback(elements):
            return elements.item.is_enabled() if elements.items else False
        return self.with_update(callback, ttl=ttl)

    def is_selected(self, ttl=None):
        """Get whether or not the element is selected

        If there are multiple items in this object, the selected state of the
        first element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``True`` if and only if the first element is select
        """
        def callback(elements):
            return elements.item.is_selected() if elements.items else False
        return self.with_update(callback, ttl=ttl)

    def text(self, ttl=None):
        """Return the text

        If there are multiple items in this object, the text of the first
        element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: The text of the first element
        """
        def callback(elements):
            return elements.item.text if elements.items else None
        return self.with_update(callback, ttl=ttl)

    def tag_name(self, ttl=None):
        """Return the tag name

        If there are multiple items in this object, the tag name of the first
        element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: The tag name of the first element
        """
        def callback(elements):
            return elements.item.tag_name if elements.items else None
        return self.with_update(callback, ttl=ttl)

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
        return self.with_update(callback, ttl=ttl)

    def attribute(self, name, ttl=None):
        """Get the attribute with the given name

        If there are multiple items in this object, the attribute of the first
        element will be returned.

        :param name: The name of the attribute
        :param ttl: The minimum number of seconds to keep retrying
        :returns: The attribute of the first element
        """
        def callback(elements):
            return elements.item.get_attribute(name) \
                   if elements.items else None
        return self.with_update(callback, ttl=ttl)

    def clear(self, ttl=None):
        """Clear the contents of the elements

        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        """
        return self.foreach(
            lambda elements: elements.item.clear(),
            ttl=ttl if ttl else self.ttl)

    def click(self, pause=0, ttl=None):
        """Click the element

        If there are multiple elements, each of the elements will be clicked

        :param pause: The number of seconds to pause between clicks if there
                      are multiple things to click
        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        """
        return self.foreach(
            lambda elements: elements.item.click(),
            pause=pause,
            ttl=ttl if ttl else self.ttl)

    def select(self, i=None, value=None, text=None, ttl=None):
        """Select the element

        If there are multiple elements, each of the elements will be selected.
        At least one of the attributes :attr:`i`, :attr:`value`, or :attr:`text`
        must be supplied

        :param i: The index to select
        :param value: The value to match against
        :param text: The visible text to match against
        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        """
        def callback(elements):
            s = Select(elements.item)
            if i:
                s.select_by_index(i)
            elif value:
                s.select_by_value(value)
            elif text:
                s.select_by_visible_text(text)
            else:
                raise ValueError("i, value, or text must be provided")
        return self.foreach(
            callback, ttl=ttl if ttl else self.ttl)

    def deselect(self, i=None, value=None, text=None, ttl=None):
        """Select the element

        If there are multiple elements, each of the elements will be deselected.
        If :attr:`i`, :attr:`value`, or :attr:`text` are not supplied, all
        values will be deselected.

        :param i: The index to select
        :param value: The value to match against
        :param text: The visible text to match against
        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        """
        def callback(elements):
            s = Select(elements.item)
            if i:
                s.deselect_by_index(i)
            elif value:
                s.deselect_by_value(value)
            elif text:
                s.deselect_by_visible_text(text)
            else:
                s.deselect_all()
        return self.foreach(
            callback, ttl=ttl if ttl else self.ttl)

    def write(self, text, ttl=None):
        """Write text to an element

        Instead of just setting the value of an item, this will "write" the
        text by simulting sending of key press commands.

        :param text: The text to write
        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        """
        return self.foreach(
            lambda elements: elements.item.send_keys(text),
            ttl=ttl if ttl else self.ttl)

    def closest(self, selector, ttl=None):
        """Find the closest element maching the selector.

        :param selector: The selector to use
        :param ttl: The minimum number of seconds to keep retrying
        :returns: The closest element maching the :attr:`selector`
        """
        raise NotImplementedError()

    def parent(self, ttl=None):
        """Get the parent element

        :param ttl: The minimum number of seconds to keep retrying
        :returns: The parent element
        """
        def callback(elements):
            return [elements.item.parent] if elements.items else None
        return SeElements(self.browser, self, callback, self.config)

    def find(self, selector, only_displayed=True, wait=False, ttl=None):
        """Find the elements that match the given selector

        :param selector: The selector to use
        :param only_displayed: Whether or not to only return elements that
                               are displayed
        :param wait: Wait until the selector finds at least 1 element. If this
                     is set to ``True``, the find is retried for the appropriate
                     number of seconds until at least 1 element is found. This
                     is different from just setting the :attr:`ttl`, as it is
                     possible to successfully return from a find with no
                     elements if the DOM is currently changing. Syntactically,
                     setting this to ``True`` is equivalent to::

                        elements.find('selector').until(lambda e: len(e) > 0)

        :param ttl: The minimum number of seconds to keep retrying
        :returns: An :class:`Elements` object containing the web elements that
                  match the :attr:`selector`
        """
        ttl = ttl if ttl else self.ttl
        def callback(elements):
            def inner(e):
                matches = e.item.find_elements_by_css_selector(selector)
                if only_displayed:
                    matches = filter(lambda obj: obj.is_displayed(), matches)
                return matches
            results = elements.foreach(
                inner,
                return_results=True,
                ttl=ttl)
            return [item for sublist in results for item in sublist]

        elements = SeElements(self.browser, self, callback, self.config)
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
        return self.find(
            selector, only_displayed=only_displayed, wait=True, ttl=ttl)\
            .insist(lambda e: e.is_displayed())

    def xpath(self, selector, only_displayed=True, wait=False, ttl=None):
        """Find the elements that match the given xpath selector

        :param selector: The selector to use
        :param only_displayed: Whether or not to only return elements that
                               are displayed
        :param wait: Wait until the selector finds at least 1 element. If this
                     is set to ``True``, the find is retried for the appropriate
                     number of seconds until at least 1 element is found. This
                     is different from just setting the :attr:`ttl`, as it is
                     possible to successfully return from a find with no
                     elements if the DOM is currently changing. Syntactically,
                     setting this to ``True`` is equivalent to::

                        elements.xpath('selector').until(lambda e: len(e) > 0)

        :param ttl: The minimum number of seconds to keep retrying
        :returns: An :class:`Elements` object containing the web elements that
                  match the :attr:`selector`
        """
        ttl = ttl if ttl else self.ttl
        def callback(elements):
            def inner(e):
                matches = e.item.find_elements_by_xpath(selector)
                if only_displayed:
                    matches = filter(lambda obj: obj.is_displayed(), matches)
                return matches
            results = elements.foreach(
                inner,
                return_results=True,
                ttl=ttl)
            return [item for sublist in results for item in sublist]

        elements = SeElements(self.browser, self, callback, self.config)
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
                     is set to ``True``, the find is retried for the appropriate
                     number of seconds until at least 1 element is found. This
                     is different from just setting the :attr:`ttl`, as it is
                     possible to successfully return from a find with no
                     elements if the DOM is currently changing. Syntactically,
                     setting this to ``True`` is equivalent to::

                        elements.
                            find_link('selector').
                            until(lambda e: len(e) > 0)

        :param ttl: The minimum number of seconds to keep retrying
        :returns: An :class:`Elements` object containing the web elements that
                  match the :attr:`selector`
        """
        ttl = ttl if ttl else self.ttl
        if exact:
            def callback(elements):
                def inner(e):
                    matches = e.item.find_elements_by_link_text(selector)
                    if only_displayed:
                        matches =\
                            filter(lambda obj: obj.is_displayed(), matches)
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
                            filter(lambda obj: obj.is_displayed(), matches)
                    return matches
                results = elements.foreach(
                    inner,
                    return_results=True,
                    ttl=ttl)
                return [item for sublist in results for item in sublist]
        
        elements = SeElements(self.browser, self, callback, self.config)
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
            filter(fn, elements)
            return elements.items
        return SeElements(self.browser, self, callback, self.config)

    def title(self, ttl=None):
        """Get the title of the page

        :param ttl: The minimum number of seconds to keep retrying
        :returns: The title of the page
        """
        def callback(elements):
            return elements.browser.title
        return self.with_update(callback, ttl=ttl)

    def source(self, ttl=None):
        """Get the source of the page

        :param ttl: The minimum number of seconds to keep retrying
        :returns: The source of the page
        """
        def callback(elements):
            return elements.browser.page_source
        return self.with_update(callback, ttl=ttl)

    def navigate(self, url, ttl=None):
        """Navigate the browser to the given URL

        :param url: The URL to navigate the browser to
        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        """
        self.with_retry(lambda: self.browser.get(url), ttl=ttl)
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
            raise NotImplementedError("Can't perform async scripts yet. Sorry.")
        ttl = ttl if ttl else self.ttl
        results = with_retry(
            lambda: self.browser.execute_script(script),
            WebDriverException, ttl=ttl)
        if not callback:
            return results
        else:
            return callback(results)

    def get_window_size(self):
        """Get the size of the browser window

        :returns: A tuple of the form ``(width, height)`` where the units are
                  pixels
        """
        try:
            dim = self.browser.get_window_size()
            return (dim['width'], dim['height'])
        except:
            pass
            
    def set_window_size(self, width, height, sleep=DEFAULT_SLEEP_TIME):
        """Set the size of the browser window

        :param width: Browser width in pixels
        :param height: Browser height in pixels
        :param sleep: The number of seconds to sleep after the command to make
                      sure the command has been run
        :returns: ``self``
        """
        try:
            self.browser.set_window_size(width, height)
            if sleep:
                time.sleep(sleep)
        except:
            pass
        return self

    def scroll(self, x=0, y=0, sleep=DEFAULT_SLEEP_TIME):
        """Scroll to the given position on the page

        :param x: The x position on the page. This can either be a number
                  (pixels from the left) or a javascript string that evalutes
                  to a position (e.g. ``document.body.scrollWidth``)
        :param y: The y position on the page. This can either be a number
                  (pixels from the top) or a javascript string that evalutes
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
                  (pixels from the left) or a javascript string that evalutes
                  to a position (e.g. ``document.body.scrollHeight``)
        :param sleep: The number of seconds to sleep after the command to make
                      sure the command has been run
        :returns: ``self``
        """
        return self.scroll(x=x, y=0, sleep=sleep)

    def scroll_bottom(self, x=0, sleep=DEFAULT_SLEEP_TIME):
        """Scroll to the bottom of the page

        :param x: The x position on the page. This can either be a number
                  (pixels from the left) or a javascript string that evalutes
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
        return self.with_retry(fn, ttl=ttl)

    def switch_to_active_element(self):
        """Get the active element

        :returns: The active element
        """
        def callback(elements):
            return [elements.item.switch_to_active_element()]\
                    if elements.items else None
        return SeElements(self.browser, self, callback, self.config)
