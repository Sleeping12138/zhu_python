import pytest


@pytest.fixture(scope="session", autouse=True)
def all_fixtures():
    print("测试开始")

    yield

    print("测试结束")