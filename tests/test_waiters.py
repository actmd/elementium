from __future__ import absolute_import

__author__ = "Patrick R. Schmid"
__email__ = "prschmid@act.md"

import time
import unittest

from mock import MagicMock

from elementium.exc import TimeOutError
from elementium.waiters import (
    ConditionElementsWaiter,
    ExceptionRetryWaiter,
    ExceptionRetryElementsWaiter,
    Waiter
)


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(WaiterTestCase))
    suite.addTest(unittest.makeSuite(ExceptionRetryWaiterTestCase))
    suite.addTest(unittest.makeSuite(ExceptionRetryElementsWaiterTestCase))
    suite.addTest(unittest.makeSuite(ConditionElementsWaiterTestCase))
    return suite


class WaiterTestImpl(Waiter):
    def wait(self, n=0, ttl=None, **kwargs):
        raise NotImplementedError()


class WaiterTestCase(unittest.TestCase):
    def test_cannot_set_both_n_and_ttl_in_init(self):
        with self.assertRaises(ValueError):
            WaiterTestImpl(n=1, ttl=1)

    def test_cannot_set_negative(self):
        with self.assertRaises(ValueError):
            WaiterTestImpl(pause=-1)
        with self.assertRaises(ValueError):
            WaiterTestImpl(n=1, ttl=-1)
        with self.assertRaises(ValueError):
            WaiterTestImpl(n=-1, ttl=1)

    def test_check_args_with_none_arguments(self):
        w = WaiterTestImpl()
        with self.assertRaises(ValueError):
            w._check_args(n=-1, ttl=-1)
        with self.assertRaises(ValueError):
            w._check_args(n=-1, ttl=None)
        with self.assertRaises(ValueError):
            w._check_args(n=None, ttl=-1)
        with self.assertRaises(ValueError):
            w._check_args(n=None, ttl=None)
        with self.assertRaises(ValueError):
            w._check_args(n=0, ttl=0)

    def test_check_args_with_both_arguments_set(self):
        with self.assertRaises(ValueError):
            WaiterTestImpl()._check_args(n=1, ttl=1)

    def test_check_args_with_valid_arguments(self):
        w = WaiterTestImpl()
        self.assertTrue(w._check_args(n=None, ttl=1))
        self.assertTrue(w._check_args(n=0, ttl=1))
        self.assertTrue(w._check_args(n=1, ttl=None))
        self.assertTrue(w._check_args(n=1, ttl=0))

    def test_check_args_does_not_allow_negative_values(self):
        w = WaiterTestImpl()
        with self.assertRaises(ValueError):
            w._check_args(n=None, ttl=-1)
        with self.assertRaises(ValueError):
            w._check_args(n=-1, ttl=None)
        with self.assertRaises(ValueError):
            w._check_args(n=1, ttl=-1)
        with self.assertRaises(ValueError):
            w._check_args(n=-1, ttl=1)


class ExceptionRetryWaiterMixin(object):
    def waiter(self, exceptions):
        raise NotImplementedError("Subclass must return appropriate waiter")

    def test_cannot_instantiate_without_exceptions(self):
        with self.assertRaises(ValueError):
            self.waiter(None)
        with self.assertRaises(ValueError):
            self.waiter([])

    def test_does_retry_for_registered_exception_with_n_retries(self):
        f = MagicMock(side_effect=TypeError('Oops'))
        with self.assertRaises(TypeError):
            self.waiter(TypeError).wait(f, n=2)
        self.assertEqual(f.call_count, 2)

    def test_does_retry_for_registered_exception_with_ttl_retries(self):
        f = MagicMock(side_effect=TypeError('Oops'))
        start_time = time.time()
        with self.assertRaises(TypeError):
            self.waiter(TypeError).wait(f, ttl=2)
        end_time = time.time()
        self.assertGreater(f.call_count, 1)
        self.assertGreaterEqual(end_time - start_time, 2)

    def test_does_retry_for_registered_exceptions(self):
        f1 = MagicMock(side_effect=TypeError('Oops'))
        f2 = MagicMock(side_effect=ValueError('Oops'))

        w = self.waiter([TypeError, ValueError])

        with self.assertRaises(TypeError):
            w.wait(f1, n=2)
        self.assertEqual(f1.call_count, 2)

        with self.assertRaises(ValueError):
            w.wait(f2, n=2)
        self.assertEqual(f2.call_count, 2)

    def test_does_not_retry_if_no_exceptions(self):
        f = MagicMock(return_value=True)
        self.waiter(TypeError).wait(f, n=2)
        self.assertEqual(f.call_count, 1)

    def test_does_raise_non_registered_exception(self):
        f = MagicMock(side_effect=ValueError('Oops'))
        with self.assertRaises(ValueError):
            self.waiter(TypeError).wait(f, n=2)
        self.assertEqual(f.call_count, 1)


class ExceptionRetryWaiterTestCase(unittest.TestCase,
                                   ExceptionRetryWaiterMixin):
    def waiter(self, exceptions):
        return ExceptionRetryWaiter(exceptions, pause=0.1)


class ExceptionRetryElementsWaiterTestCase(unittest.TestCase,
                                           ExceptionRetryWaiterMixin):
    def waiter(self, exceptions):
        return ExceptionRetryElementsWaiter(MagicMock(), exceptions, pause=0.1)

    def test_does_raises_exception_if_waiter_never_run(self):
        waiter = ExceptionRetryElementsWaiter(MagicMock(), TypeError)

        # Need to set them after the fact to circumvent the error checking
        waiter.n = -1
        waiter.ttl = -1

        with self.assertRaises(RuntimeError) as context:
            waiter.wait(MagicMock(side_effect=TypeError('Oops')), ttl=0, n=0)
        self.assertIn("Waiter was never run.", str(context.exception))


class ConditionElementsWaiterTestCase(unittest.TestCase):
    def test_does_retry_if_function_does_not_evaluate_to_true_with_n_retires(
            self):
        f = MagicMock(return_value=False)
        with self.assertRaises(TimeOutError):
            ConditionElementsWaiter(MagicMock(), pause=0.1).wait(f, n=2)
        self.assertEqual(f.call_count, 2)

    def test_does_retry_if_function_does_not_evaluate_to_true_with_ttl_retires(
            self):
        f = MagicMock(return_value=False)
        start_time = time.time()
        with self.assertRaises(TimeOutError):
            ConditionElementsWaiter(MagicMock(), pause=0.1).wait(f, ttl=2)
        end_time = time.time()
        self.assertGreaterEqual(f.call_count, 1)
        self.assertGreaterEqual(end_time - start_time, 2)

    def test_does_not_retry_if_function_evaluates_to_true(self):
        f = MagicMock(return_value=True)
        ConditionElementsWaiter(MagicMock(), pause=0.1).wait(f, n=2)
        self.assertEqual(f.call_count, 1)


if __name__ == '__main__':
    unittest.main()
