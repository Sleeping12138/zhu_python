# from jsonschema import validate
#
#
# def test_data():
#     data = {
#         "code": 200,
#         "msg": "success",
#         "data": {
#             "name": "zhangsan",
#             "age": 18
#         }
#     }
#
#     data_schema = {
#         "type": "object",
#         "properties": {
#             "code": {
#                 "type": "integer"
#             },
#             "msg": {
#                 "type": "string"
#             },
#             "data": {
#                 "type": "object",
#                 "properties": {
#                     "name": {
#                         "type": "string"
#                     },
#                     "age": {
#                         "type": "integer"
#                     }
#                 },
#                 "additionalProperties": False,
#                 "required": [
#                     "name",
#                     "age"
#                 ]
#             }
#         },
#         "additionalProperties": False,
#         "required": [
#             "code",
#             "msg",
#             "data"
#         ]
#     }
#
#     validate(data, data_schema)
#
#
