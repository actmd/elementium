"""Elemetium classes used to wait for other things to happen"""

from __future__ import absolute_import

import abc
import inspect
import six
import time

from elementium.exc import TimeOutError
from elementium.util import (
    DEFAULT_SLEEP_TIME,
    DEFAULT_TTL,
    ignored
)


__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"


class Waiter(six.with_metaclass(abc.ABCMeta, object)):
    """Wait for something to happen"""

    __metaclass__ = abc.ABCMeta

    def __init__(self, n=0, ttl=None, pause=1):
        """Create a new Waiter

        :param n: The number of times to retry.
        :param ttl: The number of seconds to wait.
        :param pause: The number of seconds to pause between retries
        """
        if n and ttl:
            raise ValueError("Cannot set both n and ttl")
        if n < 0:
            raise ValueError("n cannot be negative")
        if ttl and ttl < 0:
            raise ValueError("ttl cannot be negative")
        if pause and pause < 0:
            raise ValueError("pause cannot be negative")
        self.n = n
        self.ttl = ttl if ttl else 0
        self.pause = pause

    @abc.abstractmethod
    def wait(self, n=0, ttl=None, **kwargs):
        """Wait until a particular condition is met

        :param n: The number of times to retry. This will override what is
                  passed to the constructor
        :param ttl: The number of seconds to wait. This will override what is
                    passed to the constructor
        :param \*\*kwargs: Any other parameters
        :returns: The :class:`Elements` object that was passed to the
                  constructor
        :raise:
            :TimeOutError: If the condition is not met by the the specified
                           time/number of retries
        """
        return

    def _check_args(self, n, ttl):
        """Helper function to check the n and ttl arguments

        :param n: The number of times to retry
        :param ttl: The time to wait.
        :return: A tuple of the form ``(n, ttl)``, such that either the values
                 passed in are returned, or the ones from ``self`` are
                 returned.
        :raise:
            :ValueError: if either both n and ttl are set, neither n nor
                         ttl are set, if either n or ttl are negative
        """
        if n is not None:
            if n < 0:
                raise ValueError("n cannot be negative")
        else:
            n = 0

        if ttl is not None:
            if ttl < 0:
                raise ValueError("ttl cannot be negative")
        else:
            ttl = 0
        if n and ttl:
            raise ValueError("Cannot set both n and ttl")
        if not n and not ttl:
            if self.n or self.ttl:
                return self.n, self.ttl
            else:
                raise ValueError("Must set either n or ttl with value >= 0")
        return n, ttl


class ExceptionRetryWaiter(Waiter):

    def __init__(
            self, exceptions, n=0, ttl=DEFAULT_TTL, pause=DEFAULT_SLEEP_TIME):
        """Create a new Waiter

        :param exceptions: The exception or iterable of exceptions to retry on
        :param n: The number of times to retry.
        :param ttl: The number of seconds to wait.
        :param pause: The number of seconds to pause between retries
        """
        super(ExceptionRetryWaiter, self).__init__(n=n, ttl=ttl, pause=pause)
        if not exceptions:
            raise ValueError("Must provide exceptions to retry on")
        if not hasattr(exceptions, '__iter__'):
            exceptions = [exceptions]
        if not isinstance(exceptions, tuple):
            exceptions = tuple(exceptions)
        self.exceptions = exceptions

    def wait(self, fn, n=0, ttl=None):
        """Retry a function for :attr:`ttl` seconds

        :param fn: The function to call
        :param n: The number of times to retry. This will override what is
                  passed to the constructor
        :param ttl: The number of seconds to wait. This will override what is
                    passed to the constructor
        :returns: The result of running :attr:`fn`
        """
        n, ttl = self._check_args(n, ttl)
        etime = time.time() + ttl
        pause = self.pause
        while True:
            n -= 1
            try:
                return fn()
            except self.exceptions as exc:
                if time.time() < etime or n > 0:
                    time.sleep(pause)
                    pause = min(pause + pause, pause * 4)
                else:
                    raise exc


class ElementsWaiter(Waiter):
    """Wait for something to happen"""

    def __init__(
            self, elements, n=0, ttl=DEFAULT_TTL, pause=DEFAULT_SLEEP_TIME):
        """Create a new Waiter

        :param elements: The :class:`Elements` we want to wait on.
        :param n: The number of times to retry.
        :param ttl: The number of seconds to wait.
        :param pause: The number of seconds to pause between retries
        """
        super(ElementsWaiter, self).__init__(n=n, ttl=ttl, pause=pause)
        self.elements = elements


class ExceptionRetryElementsWaiter(ElementsWaiter):

    def __init__(
            self, elements, exceptions, n=0, ttl=DEFAULT_TTL,
            pause=DEFAULT_SLEEP_TIME):
        """Create a new Waiter

        :param elements: The :class:`Elements` we want to wait on.
        :param exceptions: The exception or iterable of exceptions to retry on
        :param n: The number of times to retry.
        :param ttl: The number of seconds to wait.
        :param pause: The number of seconds to pause between retries
        """
        super(ExceptionRetryElementsWaiter, self).__init__(
            elements=elements, n=n, ttl=ttl, pause=pause)
        if not exceptions:
            raise ValueError("Must provide exceptions to retry on")
        if not hasattr(exceptions, '__iter__'):
            exceptions = [exceptions]
        if not isinstance(exceptions, tuple):
            exceptions = tuple(exceptions)
        self.exceptions = exceptions

    def wait(self, fn, n=0, ttl=None):
        """Retry a function for :attr:`ttl` seconds

        :param fn: The function to call
        :param n: The number of times to retry. This will override what is
                  passed to the constructor
        :param ttl: The number of seconds to wait. This will override what is
                    passed to the constructor
        :returns: The result of running :attr:`fn`
        """
        n, ttl = self._check_args(n, ttl)
        etime = time.time() + ttl
        pause = self.pause
        exc_from_run = None
        while time.time() < etime or n > 0:
            n -= 1
            try:
                return fn(self.elements)
            except self.exceptions as exc:
                time.sleep(pause)
                pause = min(pause + pause, pause * 4)
                exc_from_run = exc
                if self.elements:
                    self.elements.update()
        else:
            if exc_from_run:
                raise exc_from_run
            else:
                raise RuntimeError(
                    "Waiter was never run. This could mean that the n ({}) or "
                    "ttl ({}) were negative or that your ttl was too small "
                    "causing the waiter to never to be executed.".format(
                        n, ttl))


class ConditionElementsWaiter(ElementsWaiter):
    """Wait for a condition to be met"""

    def wait(self, fn, n=0, ttl=None):
        """Wait until a particular condition is met

        :param fn: The function that corresponds to the condition that must be
                   met. Once this function returns ``True``, it will return.
                   If ``True`` is not returned in the provided amount of time,
                   a :class:`TimeOutError`
        :param n: The number of times to retry. This will override what is
                  passed to the constructor
        :param ttl: The number of seconds to wait. This will override what is
                    passed to the constructor
        :returns: The :class:`Elements` object that was passed to the
                  constructor
        """
        n, ttl = self._check_args(n, ttl)
        etime = time.time() + ttl
        pause = self.pause
        while time.time() < etime or n > 0:
            n -= 1
            if not fn(self.elements):
                time.sleep(pause)
                pause = min(pause + pause, pause * 4)
                self.elements.update()
            else:
                break
        else:
            reason = "Unknown"
            with ignored(Exception):
                reason = inspect.getsource(fn)
                reason = reason.strip()
            raise TimeOutError(reason)
        return self.elements
