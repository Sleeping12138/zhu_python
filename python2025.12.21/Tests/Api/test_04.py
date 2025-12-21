from Utils.yaml_util import write_yaml


def test01():
    data = {
        "name": "zhangsan",
        "age": 18
    }

    write_yaml(data)
