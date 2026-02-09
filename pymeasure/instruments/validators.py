#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2026 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from decimal import Decimal
from typing import Any, Callable, Sequence, Union

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias  # type: ignore

VALUES_TYPES: TypeAlias = Union[Sequence[float], list[float], range]


def strict_range(value: float, values: VALUES_TYPES) -> float:
    """Provides a validator function that returns the value
    if its value is less than or equal to the maximum and
    greater than or equal to the minimum of ``values``.
    Otherwise it raises a ValueError.

    :param float value: A value to test
    :param VALUES_TYPES values: A range of values (range, list, etc.)

    :return float: The value if it is in the range

    :raises: ValueError if the value is out of the range
    """
    if min(values) <= value <= max(values):
        return value
    else:
        raise ValueError(
            "Value of {:g} is not in range [{:g},{:g}]".format(value, min(values), max(values))
        )


def strict_discrete_range(value: float, values: VALUES_TYPES, step: float) -> float:
    """Provides a validator function that returns the value
    if its value is less than the maximum and greater than the
    minimum of the range and is a multiple of step.
    Otherwise it raises a ValueError.

    :param float value: A value to test
    :param VALUES_TYPES values: A range of values (range, list, etc.)
    :param float step: Minimum stepsize (resolution limit)

    :return float: The value if it is in the range and a multiple of step

    :raises: ValueError if the value is out of the range
    """
    # use Decimal type to provide correct decimal compatible floating
    # point arithmetic compared to binary floating point arithmetic
    if strict_range(value, values) == value and Decimal(str(value)) % Decimal(str(step)) == 0:
        return value
    else:
        raise ValueError("Value of {:g} is not a multiple of {:g}".format(value, step))


def strict_discrete_set(value: float, values: VALUES_TYPES) -> float:
    """Provides a validator function that returns the value
    if it is in the discrete set. Otherwise it raises a ValueError.

    :param float value: A value to test
    :param VALUES_TYPES values: A set of values that are valid

    :return float: The value if it is in the discrete set

    :raises: ValueError if the value is not in the set
    """
    if value in values:
        return value
    else:
        raise ValueError("Value of {} is not in the discrete set {}".format(value, values))


def truncated_range(value: float, values: VALUES_TYPES) -> float:
    """Provides a validator function that returns the value
    if it is in the range. Otherwise it returns the closest
    range bound.

    :param float value: A value to test
    :param VALUES_TYPES values: A set of values that are valid

    :return float: The value if it is in the range, otherwise the closest range bound
    """
    if min(values) <= value <= max(values):
        return value
    if value > max(values):
        return max(values)
    return min(values)


def modular_range(value: float, values: VALUES_TYPES) -> float:
    """Provides a validator function that returns the value
    if it is in the range. Otherwise it returns the value,
    modulo the max of the range.

    :param float value: a value to test
    :param VALUES_TYPES values: A set of values that are valid

    :return float: The value if it is in the range, otherwise the value modulo the max of the range
    """
    return value % max(values)


def modular_range_bidirectional(value: float, values: VALUES_TYPES) -> float:
    """Provides a validator function that returns the value
    if it is in the range. Otherwise it returns the value,
    modulo the max of the range. Allows negative values.

    :param float value: a value to test
    :param VALUES_TYPES values: A set of values that are valid

    :return float: The value if it is in the range, otherwise the value modulo the max of the range
    """
    if value > 0:
        return value % max(values)

    return -1 * (abs(value) % max(values))


def truncated_discrete_set(value: float, values: VALUES_TYPES) -> float:
    """Provides a validator function that returns the value
    if it is in the discrete set. Otherwise, it returns the smallest
    value that is larger than the value.

    :param float value: A value to test
    :param VALUES_TYPES values: A set of values that are valid

    :return float: The value if it is in the discrete set,
        otherwise the smallest value that is larger than the value
    """
    # Force the values to be sorted
    values = list(values)
    values.sort()
    for v in values:
        if value <= v:
            return v

    return values[-1]


def joined_validators(
    *validators: Callable[..., Any]
) -> Callable[[Any, Sequence[VALUES_TYPES]], Any]:
    """Returns a validator function that represents a list of validators joined together.

    A value passed to the validator is returned if it passes any validator (not all of them).
    Otherwise it raises a ValueError.

    Note: the joined validator expects ``values`` to be a sequence of ``values``
    appropriate for the respective validators (often sequences themselves).

    :Example:

    >>> from pymeasure.instruments.validators import strict_discrete_set, strict_range
    >>> from pymeasure.instruments.validators import joined_validators
    >>> joined_v = joined_validators(strict_discrete_set, strict_range)
    >>> values = [['MAX','MIN'], range(10)]
    >>> joined_v(5, values)
    5
    >>> joined_v('MAX', values)
    'MAX'
    >>> joined_v('NONSENSE', values)
    Traceback (most recent call last):
    ...
    ValueError: Value of NONSENSE does not match any of the joined validators

    :param validators: an iterable of other validators
    """

    def validate(value: Any, values: Sequence[VALUES_TYPES]) -> Any:
        for validator, vals in zip(validators, values):
            try:
                return validator(value, vals)
            except (ValueError, TypeError):
                pass
        raise ValueError(f"Value of {value} does not match any of the joined validators")

    return validate


def discreteTruncate(number: float, discrete_set: VALUES_TYPES) -> Union[float, bool]:
    """Truncates the number to the closest element in the positive discrete set.

    :param float number: The number to truncate.
    :param VALUES_TYPES discrete_set: A set of values that are valid.

    :return Union[float, bool]: The closest element in the positive discrete set if the
        number is valid, otherwise False.
    """
    if number < 0:
        return False
    discrete_set = sorted(discrete_set)
    for item in discrete_set:
        if number <= item:
            return item
    return False
