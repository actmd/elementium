"""Elementium utility functions"""

__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"

from contextlib import contextmanager
import time


DEFAULT_SLEEP_TIME = 0.25
DEFAULT_TTL = 20


@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass
