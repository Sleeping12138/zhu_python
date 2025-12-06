from jsonschema.validators import validate


def test_01():
    json_data = {
        "code": "SUCCESS",
        "errMsg": "",
        "data": False
    }

    json_schema = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string"
            },
            "errMsg": {
                "type": "string"
            },
            "data": {
                "type": "boolean"
            }
        },
    }

    validate(json_data, json_schema)

    print("验证成功")

