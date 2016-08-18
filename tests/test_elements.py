from __future__ import absolute_import

__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"

import unittest

from mock import patch

from elementium.elements import Elements


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ElementsTestCase))
    return suite


class ElementsTestImpl(Elements):
    def get(self, i): pass

    def retried(self, fn, update=True, ttl=None): pass

    def is_displayed(self, ttl=None): pass

    def is_enabled(self, ttl=None): pass

    def is_selected(self, ttl=None): pass

    def text(self, ttl=None): pass

    def tag_name(self, ttl=None): pass

    def value(self, ttl=None): pass

    def attribute(self, name, ttl=None): pass

    def clear(self, ttl=None): pass

    def click(self, ttl=None): pass

    def write(self, text, ttl=None): pass

    def closest(self, selector, ttl=None): pass

    def parent(self, ttl=None): pass

    def find(self, selector, ttl=None): pass

    def xpath(self, selector, ttl=None): pass

    def filter(self, fn, ttl=None): pass


class ElementsTestCase(unittest.TestCase):
    def test_init_items_are_loaded_by_default(self):
        with patch.object(ElementsTestImpl, 'update',
                          return_value=True) as mock_update:
            ElementsTestImpl(None, context=None, fn='.foo')
            self.assertTrue(mock_update.called)

    def test_init_items_can_be_lazy_loaded(self):
        with patch.object(ElementsTestImpl, 'update',
                          return_value=True) as mock_update:
            ElementsTestImpl(None, context=None, fn='.foo', lazy=True)
            self.assertFalse(mock_update.called)

    def test_update_is_called_on_first_access(self):
        with patch.object(ElementsTestImpl, 'update',
                          return_value=True) as mock_update:
            e = ElementsTestImpl(None, context=None, fn='.foo', lazy=True)
            self.assertFalse(mock_update.called)

            # Get the items
            e.items

            # Should be called
            self.assertTrue(mock_update.called)


if __name__ == '__main__':
    unittest.main()
