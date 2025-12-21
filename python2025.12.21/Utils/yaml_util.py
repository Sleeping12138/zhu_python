import yaml


def write_yaml(data):
    with open("./Tests/Data/data.yml", "w", encoding="utf-8") as file:
        yaml.safe_dump(data, file)


def read_yaml():
    with open("./Tests/Data/data.yml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def delete_yaml():
    with open("./Tests/Data/data.yml") as file:
        file.truncate()
