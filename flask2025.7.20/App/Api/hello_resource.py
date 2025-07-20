from flask_restful import Resource


class HelloResource(Resource):
    def get(self):
        return 'hello get'

    def post(self):
        return 'hello post'
