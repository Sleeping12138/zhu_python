from ..exts import api
from .hello_resource import *

api.add_resource(HelloResource, '/hello')