import pytest

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (1, 1, 2),
    (-1, 1, 0),
    (0, 0, 0),
    (100, 200, 300)
])

def add(x, y):
    return x + y

def test_add(a, b, expected):
    assert add(a, b) == expected


