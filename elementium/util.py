"""Elementium utility functions"""

from __future__ import absolute_import

from contextlib import contextmanager

__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"


DEFAULT_SLEEP_TIME = 0.25
DEFAULT_TTL = 20


@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass
