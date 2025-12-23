# line = 3
# i = 1
# while i <= line:
#     number = 1
#     while number <= i:
#         print("*")
#         number += 1


# s = "hello world"
# for ss in s:
#     print(ss,end=" ")
#
# print(len(s))

# sum = 0
# for i in range(1, 11):
#     sum += i
# print(sum)
#
# for i in range(10, 1, -1):
#     print(i, end=" ")

#
# sum = 0
# for i in range(50, 125, 2):
#     sum += i
# print(sum)


# for i in range(3):
#     for j in range(3 - i, 0, -1):
#         print("*", end=" ")
#     print()

for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}*{i}={i * j}", end=" ")
    print()
