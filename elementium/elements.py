"""Elementium elements"""
from __future__ import absolute_import

import abc
import collections
import six
import time

from elementium.exc import TimeOutError
from elementium.util import (
    DEFAULT_TTL,
    ignored
)
from elementium.waiters import ConditionElementsWaiter


__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"


@six.add_metaclass(abc.ABCMeta)
class Browser(object):
    """A base interface for a browser."""

    @abc.abstractmethod
    def title(self):
        """Get the title of the page"""
        return

    @abc.abstractmethod
    def source(self):
        """Get the source of the page"""
        return

    @abc.abstractmethod
    def navigate(self, url):
        """Navigate the browser to the given URL

        :param url: The URL to navigate the browser to
        :returns: ``self``
        """
        return

    @abc.abstractmethod
    def refresh(self):
        """Refresh the current page

        :returns: ``self``
        """
        return

    @abc.abstractmethod
    def current_url(self):
        """Get the current URL

        :returns: The current URL the browser is displaying
        """
        return

    @abc.abstractmethod
    def execute_script(self, script, callback=None, asynchronous=False):
        """Execute arbitrary JavaScript

        :param script: The JavaScript to execute
        :param callback: A function to execute with the results of the script.
                         This function should take a single parameter, the
                         results from the script.
        :param asynchronous: Whether or not to do it asynchronously
        :returns: If :attr:`callback` is provided, then this will return the
                  results form the callback. If not, this will return the
                  results from the script that was executed
        """
        return

    @abc.abstractmethod
    def get_window_size(self):
        """Get the size of the browser window

        :returns: A tuple of the form ``(width, height)`` where the units are
                  pixels
        """
        return

    @abc.abstractmethod
    def set_window_size(self, width, height):
        """Set the size of the browser window

        :param width: Browser width in pixels
        :param height: Browser height in pixels
        :returns: ``self``
        """
        return


class ElementsIterator(object):
    """Iterator for Elements"""

    def __init__(self, elements):
        self.elements = elements
        self.idx = -1

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        self.idx += 1
        if self.idx < len(self.elements.items):
            return self.elements[self.idx]
        else:
            raise StopIteration


@six.add_metaclass(abc.ABCMeta)
class Elements(collections.MutableSequence):
    """The abstract base class for a list of web elements"""

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

                            `lazy`: Whether or not to lazy load the items.

        :param lazy: Whether or not to lazy load the items. If this is ``True``
                     then the :attr:`fn` is evaluated on first access.
                     If, ``False``, then :attr:`fn` is evaluated right away
                     by a call to the update() method. This lazy parameter
                     can also be set in the config dict. Note, that whatever
                     is passed here will OVERWRITE what may be in the config
                     object. Note, by default lazy will be set to ``True``
        """
        super(Elements, self).__init__()
        self.browser = browser
        self.context = context
        if not fn:
            fn = lambda context: [browser]
        self.fn = fn
        self.config = config if config else {}
        if not self.config.get('ttl'):
            self.config['ttl'] = DEFAULT_TTL
        self.config['lazy'] = lazy if lazy is not None else False
        self._items = None
        if not self.lazy:
            self.items

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.items)
    def __setitem__(self, i, value): self.items[i] = value
    def __delitem__(self, i): del self.items[i]
    def __getitem__(self, i): return self.get(i)
    def __len__(self): return len(self.items)
    def __iter__(self): return ElementsIterator(self)
    def __contains__(self, item): return item in self.items
    def insert(self, index, value): self.items.insert(index, value)

    @property
    def items(self):
        """The items that this elements object refers to"""
        if not self._items:
            self.update(propagate=False)
        return self._items

    @property
    def item(self):
        """Shorthand for first item in ``self.items``. I.e. ``self.items[0]``"""
        return self.items[0] if self.items else None

    @property
    def ttl(self):
        """The default ttl"""
        return self.config['ttl']

    @ttl.setter
    def ttl(self, value):
        """The default ttl"""
        self.config['ttl'] = value

    @property
    def lazy(self):
        """The default lazy"""
        return self.config['lazy']

    @lazy.setter
    def lazy(self, value):
        """The default lazy"""
        self.config['lazy'] = value

    @abc.abstractmethod
    def get(self, i):
        """Get the i-th item as an :class:`Elements` object

        Since the items that we store are the raw web elements returned by the
        driver, this method will wrap them appropriately, to return a
        :class:`Elements` object.

        :param i: The index of the item to return
        :returns: The item as an :class:`Elements` object
        """
        return

    @abc.abstractmethod
    def retried(self, fn, update=True, ttl=None):
        """Retry a function for :attr:`ttl` seconds

        :param fn: The function to call
        :param update: Whether or not to call update() on self between each
                       retry.
        :param ttl: The number of seconds to retry.
        :returns: The result of running :attr:`fn`
        """
        return

    @abc.abstractmethod
    def is_displayed(self, ttl=None):
        """Get whether or not the element is visible

        If there are multiple items in this object, the visibility of the first
        element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``True`` if and only if the first element is visible
        """
        return

    @abc.abstractmethod
    def is_enabled(self, ttl=None):
        """Get whether or not the element is enabled

        If there are multiple items in this object, the status of the first
        element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``True`` if and only if the first element is enabled
        """
        return

    @abc.abstractmethod
    def is_selected(self, ttl=None):
        """Get whether or not the element is selected

        If there are multiple items in this object, the status of the first
        element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``True`` if and only if the first element is selected
        """
        return

    @abc.abstractmethod
    def text(self, ttl=None):
        """Return the text

        If there are multiple items in this object, the text of the first
        element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: The text of the first element
        """
        return

    @abc.abstractmethod
    def tag_name(self, ttl=None):
        """Return the tag name

        If there are multiple items in this object, the tag name of the first
        element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: The tag name of the first element
        """
        return

    @abc.abstractmethod
    def value(self, ttl=None):
        """Get the value

        If there are multiple items in this object, the value of the first
        element will be returned.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: The value of the first element
        """
        return

    @abc.abstractmethod
    def attribute(self, name, ttl=None):
        """Get the attribute with the given name

        If there are multiple items in this object, the attribute of the first
        element will be returned.

        :param name: The name of the attribute
        :param ttl: The minimum number of seconds to keep retrying
        :returns: The attribute of the first element
        """
        return

    @abc.abstractmethod
    def clear(self, ttl=None):
        """Clear the contents of the element

        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        """
        return

    @abc.abstractmethod
    def click(self, ttl=None):
        """Click the element

        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        """
        return

    @abc.abstractmethod
    def write(self, text, ttl=None):
        """Write text to an element

        Instead of just setting the value of an item, this will "write" the
        text by simulating sending of key press commands.

        :param text: The text to write
        :param ttl: The minimum number of seconds to keep retrying
        """
        return

    @abc.abstractmethod
    def closest(self, selector, ttl=None):
        """Find the closest element matching the selector.

        :param selector: The selector to use
        :param ttl: The minimum number of seconds to keep retrying
        :returns: The closest element matching the :attr:`selector`
        """
        return

    @abc.abstractmethod
    def parent(self, ttl=None):
        """Get the parent element

        :returns: The parent element
        :param ttl: The minimum number of seconds to keep retrying
        """
        return

    @abc.abstractmethod
    def find(self, selector, ttl=None):
        """Find the elements that match the given selector

        :param selector: The selector to use
        :param ttl: The minimum number of seconds to keep retrying
        :returns: An :class:`Elements` object containing the web elements that
                  match the :attr:`selector`
        """
        return

    @abc.abstractmethod
    def xpath(self, selector, ttl=None):
        """Find the elements that match the given xpath selector

        :param selector: The selector to use
        :param ttl: The minimum number of seconds to keep retrying
        :returns: An :class:`Elements` object containing the web elements that
                  match the :attr:`selector`
        """
        return

    @abc.abstractmethod
    def filter(self, fn, ttl=None):
        """Filter the elements and return only the ones that match the filter

        :param fn: The filter function
        :param ttl: The minimum number of seconds to keep retrying
        """
        return

    def foreach(self, fn, return_results=False, pause=0, ttl=None):
        """Apply the given function to each item.

        This will make sure that each item is actually an Element object and
        not the underlying type.

        :param fn: The function to apply. This function should be of the form:

                        def myFun(elements):
                            pass

                    Where ``len(elements) == 1``. I.e it only has one
                    underlying item.

        :param return_results: Whether or not to return the results of calling
                               :attr:`fn` on each of the items.
        :param pause: The number of seconds to pause between attempting each
                      to run the :attr:`fn` for each item. This is included
                      in the :attr:`ttl` calculation.
        :param ttl: The minimum number of seconds to keep retrying
        :returns: If :attr:`return_results` is ``True``, then this will return
                  a list of length equal to ``len(self)`` where the i-th entry
                  in the list is the result of calling :attr:`fn` on the i-th
                  item in ``self``. If :attr:`return_results` is ``False``,
                  then ``self`` is returned.
        """
        ttl = ttl if ttl is not None else self.ttl
        retvals = []
        start_time = time.time()
        for element in self:
            if ttl:
                ttl = ttl - (time.time() - start_time)
            retvals.append(element.retried(fn, update=True, ttl=ttl))
            if pause:
                time.sleep(pause)
        if return_results:
            return retvals
        else:
            return self

    def until(self, fn, ttl=None):
        """Wait until a particular condition is met

        :param fn: A function that describes the condition that must be
                   met before we can return the elements. E.g. if the page
                   is loading and we need to get all links (and we know that
                   there should be three, but the third one takes a while
                   to load), we could do something like::

                    links = elements.
                        find('a').
                        until(lambda e: len(e) == 3)

                    The function takes one parameter, an Elements object.

        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        :raise:
            :TimeOutError: If the time runs out
        """
        ttl = ttl if ttl is not None else self.ttl
        return ConditionElementsWaiter(self).wait(fn, ttl=ttl)

    def insist(self, fn, ttl=None):
        """Wait until a particular condition is met and then assert

        This is very similar to :meth:`until` with the only difference being
        that it will perform an ``assert`` instead of raising a TimeOutError.

        Yes, yes. It would have been nice to call this method `assert`, but
        that unfortunately is a reserved keyword, so you'll have to make due.

        :param fn: A function that describes the condition that must be
                   met before we can return the elements. E.g. if the page
                   is loading and we need to get all links (and we know that
                   there should be three, but the third one takes a while
                   to load), we could do something like::

                    links = elements.
                        find('a').
                        insist(lambda e: len(e) == 3)

                    The function takes one parameter, an Elements object and
                    should return True or False

        :param ttl: The minimum number of seconds to keep retrying
        :returns: ``self``
        """
        ttl = ttl if ttl is not None else self.ttl
        with ignored(TimeOutError):
            ConditionElementsWaiter(self).wait(fn, ttl=ttl)
        assert fn(self)
        return self

    def update(self, propagate=True):
        """Refresh the list of web elements

        :param propagate: Whether or not to update the context's elements as
                          well
        :returns: ``self``
        """
        if propagate and self.context:
            self.context.update(propagate=True)
        self._items = self.fn(self.context)
        return self
