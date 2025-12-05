import pytest


#
#
# @pytest.mark.parametrize("data", (1, 2, 3, 4))
# def test_1(data):
#     print("data:", data)
#
#
# # @pytest.mark.parametrize("username,password", [("zhangsan", "123456"), ("lisi", "asdfgh")])
#
# pytestmark = pytest.mark.parametrize("username,password", [("zhangsan", "123456"), ("lisi", "asdfgh")])
#
#
# class Test01:
#     def test_01(self, username, password):
#         print("username:", username, "password:", password)
#
#     def test_02(self, username, password):
#         print("username:", username, "password:", password)


def data_source():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9]


@pytest.mark.parametrize("data", data_source())
def test_data_source(data):
    print("data:", data)
