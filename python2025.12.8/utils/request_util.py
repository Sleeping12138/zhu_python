import requests
from config.config import settings
from utils.logger_util import LoggerUtil


class HttpRequest:
    def __init__(self, prefix, headers=None):
        self.url = settings.BASE_URL + prefix
        self.headers = headers
        self.logger = LoggerUtil(name='http_request')

    def get(self, path):
        self.logger.info(f"调用GET接口：{self.url}")
        return requests.get(self.url + path, headers=self.headers, timeout=10)

    def post(self, path, data=None, json=None):
        self.logger.info(f"调用POST接口：{self.url} - data为：{data} - JSON为：{json}")
        return requests.post(self.url + path, headers=self.headers, data=data, json=json, timeout=10)
