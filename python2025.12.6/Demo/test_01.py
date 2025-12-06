import pytest


# @pytest.fixture
# def fixture_test01():
#     print("fixture_test01")
#
#
# @pytest.fixture
# def fixture_test02(fixture_test01):
#     print("fixture_test02")
#
#
# def test01(fixture_test02):
#     # 会先运行fixture_test01，再运行fixture_test02,再运行test01
#     print("test01")


# @pytest.fixture
# def fixture_test01():
#     print("fixture_test01")
#
#     yield
#
#     print("fixture_test01_final")
#
#
# @pytest.fixture
# def fixture_test02():
#     print("fixture_test02")
#
#     yield
#
#     print("fixture_test02_final")
#
#
# def test_01(fixture_test01, fixture_test02):
#     print("test_01")
