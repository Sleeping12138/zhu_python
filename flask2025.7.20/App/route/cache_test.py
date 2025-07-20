import time

from flask import Blueprint
from App.exts import cache

ct = Blueprint('cache_test', __name__)


@ct.route('/cache')
@cache.cached(timeout=6)
def cache():
    # time.sleep(4)
    return 'cache'


@ct.before_request
def before_request():
    print('before_request')
