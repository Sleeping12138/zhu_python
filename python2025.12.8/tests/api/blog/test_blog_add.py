import pytest
from utils.logger_util import LoggerUtil
from utils.request_util import HttpRequest
from utils.yaml_util import yaml_util


class TestBlogAdd:
    logger = LoggerUtil(name='blog')

    user_token = yaml_util.read_yaml('/tests/data/data.yaml')

    http_client = HttpRequest(prefix='/blog', headers={'user_token_header': user_token})

    @pytest.mark.parametrize('title,content', [
        ('测试添加博客1', '测试添加博客内容1'),
        ('测试添加博客2', '测试添加博客内容2'),
    ])
    def test_blog_add(self, title, content):
        """
        添加博客接口
        :return:
        """
        json_data = {
            "title": title,
            "content": content,
        }
        ret = self.http_client.post(path='/add', json=json_data)
        # 检查响应状态码
        self.logger.info(f"响应状态码: {ret.status_code}")
        self.logger.info(f"响应结果: {ret}")
