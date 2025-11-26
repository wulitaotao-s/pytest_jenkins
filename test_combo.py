import pytest

@pytest.fixture
def setup_data():
    print("准备测试数据")
    yield
    print("清理测试数据")

@pytest.mark.parametrize("input, expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("pytest", "PYTEST")
])

def test_upper(input, expected, setup_data):
    assert input.upper() == expected