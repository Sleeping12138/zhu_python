import asyncio


async def greet(name, time):
    await asyncio.sleep(time)
    return f"Hello {name}"


async def main():
    async with asyncio.TaskGroup() as group:
        task1 = group.create_task(greet("zhangsan", 1))
        task2 = group.create_task(greet("lisi", 2))

    print(task1.result())
    print(task2.result())


if __name__ == '__main__':
    asyncio.run(main())
