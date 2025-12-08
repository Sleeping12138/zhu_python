import pytest


@pytest.fixture(scope="class")
def user_login_fixture():
    print("用户登录测试开始")

    yield

    print("用户登录测试结束")
