from flask import Blueprint
from flask import jsonify
from flask import request,respose
import requests

bp = Blueprint('test', __name__)


@bp.route('/hello')
def hello_world():  # put application's code here
    return jsonify({'msg': 'hello world'})


# @bp.route('/test', methods=['GET', 'POST'])
# def test():
#     response = requests.get('http://localhost:5000/hello')
#     print(response)
#     print(response.status_code)
#     # print(response.text)
#     print(response.json())
#     return '测试完成'


@bp.route('/test', methods=['GET', 'POST'])
def test():
    print(request.method)
    print(request.args)
    print(request.form)
    print(request.json['name'])
    print(request.url)
    print(request.json)
    print(respose)

    return '测试完成'
