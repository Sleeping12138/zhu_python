import asyncio
import time
from utils import *


def get_url(url):
    print(f'开始获取{url}')
    # 同步阻塞2s
    time.sleep(2)
    print(f'结束获取{url}')
    return 'success'


async def greet(name, time):
    await asyncio.sleep(time)
    print(f'Hello {name}')


@async_timed
async def main():
    result1 = await asyncio.to_thread(get_url, 'http://www.baidu.com')
    result2 = await greet('zhangsan',1)
    print(result1)
    print(result2)


if __name__ == '__main__':
    asyncio.run(main())

