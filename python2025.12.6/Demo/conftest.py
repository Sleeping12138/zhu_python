import pytest


@pytest.fixture(scope='session', autouse=True)
def fixture_all():
    print('测试开始')

    yield

    print('测试结束')
