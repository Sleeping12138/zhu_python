import pytest
from utils.logger_util import LoggerUtil
from utils.request_util import HttpRequest
from utils.yaml_util import yaml_util


@pytest.mark.usefixtures("user_login_fixture")
class TestUserLogin:
    logger = LoggerUtil(name='user')

    http_client = HttpRequest(prefix='/user')

    # @pytest.mark.parametrize('username,password', [
    #     ('zhangsan', 123456),
    #     ('lisi', 123456)
    # ])
    # def test_login_success(self, username, password):
    #     """
    #     登录成功接口
    #     :param username:
    #     :param password:
    #     :return:
    #     """
    #     param = {
    #         "username": username,
    #         "password": password
    #     }
    #     ret = self.http_client.post(path='/login', data=param)
    #     result = ret.json()
    #     assert result["code"] == 'SUCCESS'
    #     assert result["data"] is not None
    #
    # @pytest.mark.parametrize('username,password', [
    #     ('wangwu', 123456),
    #     ('zhaoliu', 123456)
    # ])
    # def test_login_fail(self, username, password):
    #     """
    #     登录失败接口
    #     :return:
    #     """
    #     param = {
    #         "username": username,
    #         "password": password
    #     }
    #     ret = self.http_client.post(path='/login', data=param)
    #     result = ret.json()
    #     self.logger.info(result)
    #     assert result["code"] == 'FAIL'
    #     assert result["data"] is None

    @pytest.mark.parametrize("username,password,exc", [
        ("zhangsan", "123456", 'SUCCESS'),
        ("lisi", "123456", 'SUCCESS'),
        ("wangwu", "123456", 'FAIL')
    ])
    def test_login(self, username, password, exc):
        param = {
            "username": username,
            "password": password
        }
        ret = self.http_client.post(path='/login', data=param)
        result = ret.json()
        self.logger.info(result)
        assert result["code"] == exc

        if exc == 'SUCCESS':
            yaml_util.write_yaml('/tests/data/data.yaml', result["data"])
