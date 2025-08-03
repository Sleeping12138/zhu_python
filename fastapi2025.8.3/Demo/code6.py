import asyncio
from utils import async_timed


async def greet(name, time):
    await asyncio.sleep(time)
    return f"Hello {name}"


# async def main():
#     ret = await greet('zhangsan', 1)
#     print(ret)

# @async_timed
# async def main():
#     # 使用create_task可以实现并发
#     task1 = asyncio.create_task(greet('zhangsan', 1))
#     task2 = asyncio.create_task(greet('lisi', 2))
#
#     ret1 = await task1
#     ret2 = await task2
#
#     print(ret1)
#     print(ret2)

# @async_timed
# async def main():
#     async with asyncio.TaskGroup() as group:
#         task1 = group.create_task(greet('zhangsan', 1))
#         task2 = group.create_task(greet('lisi', 2))
#
#     print(task1.result())
#     print(task2.result())


# async def main():
#     try:
#         results = await asyncio.gather(
#             greet("Alice", 1),
#             greet("Bob", 2),
#             greet("Charlie", 3),
#             return_exceptions=True,
#         )
#     except:
#         pass
#
#     print(results)
#
#     tasks = asyncio.all_tasks()
#     for task in tasks:
#         if task.get_name() != 'Task-1':
#             print(task.done())
#             ret = await task
#             print(ret)


# @async_timed
# async def main():
#     coros = [
#         greet("Alice", 1),
#         greet("Bob", 2),
#         greet("Charlie", 3)
#     ]
#
#     for coro in asyncio.as_completed(coros):
#         ret = await coro
#         print(ret)


# async def main():
#     try:
#         result = await asyncio.wait_for(greet('zhangsan', 1), timeout=2)
#         print(result)
#     except asyncio.TimeoutError as e:
#         print(e)


async def main():
    coros = [
        asyncio.create_task(greet("Alice", 1)),
        asyncio.create_task(greet("Bob", 2)),
        asyncio.create_task(greet("Charlie", 3))
    ]

    done_task, pending_task = await asyncio.wait(coros, timeout=2,return_when=asyncio.ALL_COMPLETED)
    print(done_task)

    tasks = asyncio.all_tasks()
    print(tasks)

    for task in pending_task:
        if task.get_name() != 'Task-1':
            print(task.get_name())
            ret = await task
            print(ret)


if __name__ == '__main__':
    asyncio.run(main())
