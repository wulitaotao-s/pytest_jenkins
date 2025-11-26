import pytest

@pytest.fixture
def shared_fixture():
    print("全局 fixture")
    return "shared"