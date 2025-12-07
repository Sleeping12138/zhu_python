import pytest


@pytest.fixture(scope="session", autouse=True)
def session_fixture():
    """
    用于全局测试开始和结束
    """
    # 测试会话开始
    print("测试会话开始")

    yield

    # 测试会话结束
    print("测试会话结束")
