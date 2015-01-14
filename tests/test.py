from nose.tools import assert_true, assert_false

# Here's our "unit".
def IsOdd(n):
    return n % 2 == 1

# Here's our "unit tests".
class TestIsOdd():

    def test_odd_number_is_odd(self):
        assert_true(IsOdd(1))

    def test_even_number_is_not_odd(self):
        assert_false(IsOdd(2))