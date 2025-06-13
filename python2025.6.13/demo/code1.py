# 文件操作
# file = open('./test.txt','w',encoding='utf-8')
# for i in range(10):
#     file.write('hello world\n')
# file.close()
import os

# file = open('./test.txt','a',encoding='utf-8')
# for i in range(5):
#     file.write('test')
#
# file.close()

#
# file = open('./test.txt','r',encoding='utf-8')
# # ret = file.read()
# # print(ret)
#
# # res = file.readlines()
# # for text in res:
# #     print(text,end='')
# #
#
# res= file.readline()
# print(res)
#
# file.close()
#
# if os.path.exists('./test.txt'):
#     os.remove('./test.txt')
# else:
#     print('file is not exists')

# if os.path.isdir('./test'):
#     print("文件夹已存在")
# else:
#     os.mkdir('./test')

# if os.path.isdir('./aa/bb/cc'):
#     print("文件夹已存在")
# else:
#     os.makedirs('./aa/bb/cc')

# if os.path.isdir('./aa/bb/cc'):
#     os.removedirs('./aa/bb/cc')
# else:
#     print("文件夹不存在")
#
# import time
# file = os.stat('./hello.txt')
# print(file.st_size)
# print(time.ctime(file.st_atime))
# print(time.ctime(file.st_mtime))
# print(time.ctime(file.st_ctime))

# with open('./hello.txt','r',encoding='utf') as f:
#     print(f.read())

# print(f.closed())

# file_source_path = 'E:\图片保存处\微信图片_20230829192435.jpg'
# file_target_path = 'E:\图片保存处\\newPhoto.jpg'
#
# file_source = open(file_source_path, 'rb')
# file_target = open(file_target_path, 'wb')
#
# data = file_source.read()
# file_target.write(data)
#
# file_source.close()
# file_target.close()

# print("调试开始")
# i = 0
# for k in range(10):
#     i += 1
#     print(f"{i}")
#
# print("调试结束")

# num = 100
#
#
# def fun():
#     global num
#     num += 1
#
#
# for i in range(10):
#     fun()

# print(num)

# num = 2
#
#
# def fun():
#     num += 1
#
#
# fun()
