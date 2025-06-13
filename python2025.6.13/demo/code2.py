# def fun(number):
#     def fun2(num):
#         print(num + number)
#
#     return fun2
#
#
# f = fun(10)
# f(1)
# f(2)
# f(3)
# f(4)

# def fun(number):
#     def fun2(num):
#         nonlocal number
#         number = num + 1
#
#     print(number)
#     fun2(10)
#     print(number)
#
#     return fun2
#
#
# fun(10)

# def fun(fn):
#     def inner():
#         print("新增模块")
#         fn()
#
#     return inner
#
#
# def comment():
#     print('comment')
#
#
# comment = fun(comment)
# comment()


# def fun(fn):
#     def inner():
#         print("hello world")
#         fn()
#     return inner
#
# @fun
# def comment():
#     print("comment")
#
# comment()


# def fun1(fn):
#     def inner1():
#         print('inner1')
#         fn()
#
#     return inner1
#
#
# def fun2(fn):
#     def inner2():
#         print('inner2')
#         fn()
#
#     return inner2
#
#
# @fun1
# @fun2
# def comment():
#     print('comment')
#
# comment()

def fun(fn):
    def inner(*args, **kwargs):
        return fn(*args, **kwargs)

    return inner


@fun
def comment(*args, **kwargs):
    print('comment')


comment()
