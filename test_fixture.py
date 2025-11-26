import pytest

@pytest.fixture
def setup_data():
    print("准备测试数据")
    data = {"username": "admin", "password": "123456"}
    yield data
    print("清理测试数据")

def test_login(setup_data):
    assert setup_data["username"] == "admin"
