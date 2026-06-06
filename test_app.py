from app import add_numbers

def test_add_numbers_success():
    # Verify that the addition function computes correctly
    assert add_numbers(5, 7) == 12

def test_add_numbers_negative():
    # Verify that the function works with negative numbers
    assert add_numbers(-1, 1) == 0
