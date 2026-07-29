"""
test_formatting.py
Tests for utils.formatting.parse_clp_amount.
"""
import pytest

from utils.formatting import parse_clp_amount


def test_parse_simple_amount():
    assert parse_clp_amount("5000") == 5000.0


def test_parse_thousands_separator():
    assert parse_clp_amount("15.000") == 15000.0


def test_parse_decimal_comma():
    assert parse_clp_amount("1500,50") == 1500.5


def test_parse_thousands_and_decimal():
    assert parse_clp_amount("15.000,50") == 15000.5


def test_parse_invalid_raises_value_error():
    with pytest.raises(ValueError):
        parse_clp_amount("abc")
