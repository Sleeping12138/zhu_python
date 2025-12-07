import requests
from config.config import settings
from utils.logger_util import LoggerUtil


class HttpRequest:
    def __init__(self, path, headers=None):
        self.url = settings.BASE_URL + path
        self.headers = headers
        self.logger = LoggerUtil(name='http_request')

    def get(self):
        self.logger.info(f"调用GET接口：{self.url}")
        return requests.get(self.url, headers=self.headers, timeout=10)

    def post(self, data=None):
        self.logger.info(f"调用POST接口：{self.url} - 参数为：{data}")
        return requests.post(self.url, headers=self.headers, json=data, timeout=10)
