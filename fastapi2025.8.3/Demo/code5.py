import asyncio


async def greet(name, time):
    await asyncio.sleep(time)
    return f"Hello, {name}"

async def test():
    ret1 = await greet("Alice", 1)
    ret2 = await greet("Bob", 2)
    ret3 = await greet("Charlie", 3)
    print(ret1)
    print(ret2)
    print(ret3)

async def main():async def main():
    try:
        results = await asyncio.gather(
            greet("Alice", 1),
            greet("Bob", 2),
            greet("Charlie", 3),
            return_exceptions=True
        )
    except:
        pass

    print(results)

    tasks = asyncio.all_tasks()
    for task in tasks:
        if task.get_name() != 'Task-1':
            ret = await task
            print(ret)

if __name__ == '__main__':
    asyncio.run(main())

    try:
        coros = [
            greet("Alice", 1),
            greet("Bob", 2),
            greet("Charlie", 3)
        ]

        for coro in asyncio.as_completed(coros,timeout=2):
            ret = await coro
            print(ret)
    except:
        pass


    tasks = asyncio.all_tasks()

    for task in tasks:
        if task.get_name() != 'Task-1':
            print('timeout')
            ret = await task
            print(ret)


if __name__ == "__main__":
    asyncio.run(main())
