from __future__ import absolute_import

__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"

import unittest

from mock import patch

from elementium.drivers.se import SeElements


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SeElementsTestCase))
    return suite


class SeElementsTestCase(unittest.TestCase):
    def test_init_items_are_loaded_by_default(self):
        with patch.object(SeElements, 'update',
                          return_value=True) as mock_update:
            SeElements(None, context=None, fn='.foo')
            self.assertTrue(mock_update.called)

    def test_init_items_can_be_lazy_loaded(self):
        with patch.object(SeElements, 'update',
                          return_value=True) as mock_update:
            SeElements(None, context=None, fn='.foo', lazy=True)
            self.assertFalse(mock_update.called)

    def test_update_is_called_on_first_access(self):
        with patch.object(SeElements, 'update',
                          return_value=True) as mock_update:
            e = SeElements(None, context=None, fn='.foo', lazy=True)
            self.assertFalse(mock_update.called)

            # Get the items
            e.items

            # Should be called
            self.assertTrue(mock_update.called)


if __name__ == '__main__':
    unittest.main()
