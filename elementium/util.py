"""Elementium utility functions"""

__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"

from contextlib import contextmanager


@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass
