"""Elementium exceptions"""

__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"


class ElementiumError(Exception):
    """Base exception for all Elementium related errors"""
    pass


class TimeOutError(ElementiumError):
    """A timeout error"""
    pass
