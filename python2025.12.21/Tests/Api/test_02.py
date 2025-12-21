# import pytest
#
# # pytestmark = pytest.mark.parametrize("username,password", [("zhangsan", 123456), ("lisi", 123456)])
#
#
# def get_source():
#     return {
#         "username": "zhangsan",
#         "password": "123456"
#     }
#
#
# # @pytest.mark.parametrize("username,password", [("zhangsan", 123456), ("lisi", 123456)])
# @pytest.mark.parametrize("data", get_source())
# def test_user_login(data):
#     print(data.get("username"), data.get("password"))
