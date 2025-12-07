import pytest
from utils.logger_util import LoggerUtil


@pytest.mark.usefixtures("user_class_fixture")
class TestUserLogin:
    logger = LoggerUtil("user_test")

    def test_user_login(self):
        """
        测试用户登录
        """
        self.logger.info("test_user_login")


