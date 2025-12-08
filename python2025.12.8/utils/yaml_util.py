import yaml


class YamlUtil:
    """
    yaml工具类
    """

    def write_yaml(self, file_path, data):
        """
        写入yaml文件
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, allow_unicode=True)

    def read_yaml(self, file_path):
        """
        读取yaml文件
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def delete_yaml(self, file_path):
        """
        删除yaml文件
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            f.truncate()


yaml_util = YamlUtil()
