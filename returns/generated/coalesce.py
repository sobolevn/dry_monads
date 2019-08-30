# -*- coding: utf-8 -*-

from typing import Callable, TypeVar

from returns.maybe import Maybe
from returns.pipeline import is_successful
from returns.result import Result

# Contianer internals:
_ValueType = TypeVar('_ValueType')
_ErrorType = TypeVar('_ErrorType')

# Aliases:
_FirstType = TypeVar('_FirstType')

_coalesce_doc = """
Accepts two functions that handle different cases of containers.

First one handles successful containers like ``Some`` and ``Success``,
and second one for failed containers like ``Nothing`` and ``Failure``.

This function is useful when you need
to coalesce two possible container states into one type.
"""


def _coalesce(success_handler, failure_handler):
    """
    We need this function, because we cannot use a single typed function.

    .. code:: python

      >>> from returns.result import Success, Failure
      >>> f1 = lambda x: x + 1
      >>> f2 = lambda y: y + 'b'
      >>> _coalesce_result(f1, f2)(Success(1)) == 2
      True
      >>> _coalesce_result(f1, f2)(Failure('a')) == 'ab'
      True

      >>> from returns.maybe import Some, Nothing
      >>> f1 = lambda x: x + 1
      >>> f2 = lambda _: 'a'
      >>> _coalesce_maybe(f1, f2)(Some(1)) == 2
      True
      >>> _coalesce_maybe(f1, f2)(Nothing) == 'a'
      True

    """
    def decorator(container):
        if is_successful(container):
            return success_handler(container.unwrap())
        return failure_handler(container.failure())
    return decorator


_coalesce_result: Callable[
    [
        Callable[[_ValueType], _FirstType],
        Callable[[_ErrorType], _FirstType],
    ],
    Callable[[Result[_ValueType, _ErrorType]], _FirstType],
] = _coalesce
_coalesce_result.__doc__ = _coalesce_doc

_coalesce_maybe: Callable[
    [
        Callable[[_ValueType], _FirstType],
        Callable[[None], _FirstType],
    ],
    Callable[[Maybe[_ValueType]], _FirstType],
] = _coalesce
_coalesce_maybe.__doc__ = _coalesce_doc
