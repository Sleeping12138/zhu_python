import pytest


# @pytest.fixture
# def fixture_demo():
#     print("this is a fixture")


# @pytest.fixture
# def fixture_demo():
#     print("this is a fixture1")
#
#     yield
#
#     print("this is a teardown1")
#
#
# @pytest.fixture
# def fixture_demo2():
#     print("this is a fixture2")
#
#     yield
#
#     print("this is a teardown2")
#
#
# def test01(fixture_demo, fixture_demo2):
#     print("this is a test")


# @pytest.fixture(params=[1, 2, 3])
# def get_source(request):
#     return request.param

#
# def test01(get_source):
#     assert get_source >= 0

#
# def test01():
#     print("this is a test")