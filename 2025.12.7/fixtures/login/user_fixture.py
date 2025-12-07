import pytest


@pytest.fixture(scope="class", autouse=True)
def user_class_fixture():
    print("开始执行用户类测试")
    yield
    print("结束执行用户类测试")

