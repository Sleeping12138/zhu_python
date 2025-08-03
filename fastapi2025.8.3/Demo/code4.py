import asyncio


async def greet(name, time):
    await asyncio.sleep(time)
    print(f'Hello {name}')


async def greet_group(name, time):
    await asyncio.sleep(time)
    if name == 'xx':
        raise ValueError('名称错误!')
    print(f'Hello {name}')


async def main():
    try:
        results = await asyncio.gather(
            greet_group('xx', 1),
            greet('yy', 2),
            greet('zz', 2)
        )
    except:
        pass

    tacks = asyncio.all_tasks()

    for task in tacks:
        print(task.get_name())

        if task.get_name() == 'Task-1':
            continue

        ret = await task
        print(ret)


if __name__ == '__main__':
    asyncio.run(main())
