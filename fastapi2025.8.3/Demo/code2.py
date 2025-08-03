import asyncio


async def greet(name,time):
    await asyncio.sleep(time)
    return f'hello {name}'


async def main():
    # 这样时长为2秒
    task1 = asyncio.create_task(greet('zhagnsan',1))
    task2 = asyncio.create_task(greet('lisi',2))

    ret1 = await task1
    ret2 = await task2

    print(ret1,ret2)

if __name__ == '__main__':
    asyncio.run(main())


