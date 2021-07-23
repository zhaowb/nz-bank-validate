import pytest
from nz_bank_validate import nz_bank_validate


def test_examples():
    """examples from official pdf document"""
    assert nz_bank_validate(*'01-902-0068389-00'.split('-'))
    assert nz_bank_validate(*'08-6523-1954512-001'.split('-'))
    assert nz_bank_validate(*'26-2600-0320871-032'.split('-'))

def test_invalid_numbers():
    """test invalid numbers"""
    with pytest.raises(ValueError) as exc_info:
        nz_bank_validate(*'03-0001-0016527-000'.split('-'))

def test_invalid_numbers_return_on_fail():
    """test invalid numbers"""
    assert nz_bank_validate(*'03-0001-0016527-000'.split('-'), return_false_on_fail=True) is False
