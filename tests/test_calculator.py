import pytest

from learning_tools.calculator import add, divide, multiply, subtract

# Alphabetical order (Preferred for clean code)


def test_add_returns_sum_of_two_numbers():
    assert add(10, 5) == 15


def test_add_handles_negative_numbers():
    assert add(-10, 5) == -5


def test_subtract_returns_difference_of_two_numbers():
    assert subtract(20, 10) == 10


def test_subtract_handle_negative_value():
    assert subtract(5, 10) == -5


def test_multiply_returns_multiply_of_two_numbers():
    assert multiply(10, 3) == 30


def test_multiply_handle_single_negative_number():
    assert multiply(5, -5) == -25


def test_multiply_handle_two_negative_numbers():
    assert multiply(-6, -7) == 42


def test_divide_returns_quotient():
    assert divide(10, 2) == 5


def test_divide_raises_error_for_zero_denominator():
    with pytest.raises(ValueError, match="Denominator can not be zero."):
        divide(10, 0)


def test_divide_handles_negative_values():
    assert divide(-12, 3) == -4


def test_divide_returns_fractional_result():
    assert divide(7, 2) == 3.5


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(4, 3) == 12


def test_divide():
    assert divide(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Denominator can not be zero."):
        divide(10, 0)
