# with open('../tmp_01.txt', 'r', encoding='utf-8') as file:
#     while True:
#         line = file.readline()
#         if not line:
#             break
#         print(line, end='')


file1 = open('../files/tmp_01.txt', 'r', encoding='utf-8')
content = file1.read()
print(content)
file1.close()


file2 = open('../files/tmp_02.txt', 'w', encoding='utf-8')
file2.write('Happy New Year')
file2.close()


file3 = open('../files/tmp_03.txt', 'r', encoding='utf-8')
content = file3.read()
file3.close()
new_content = content.replace('python', 'world')
file3 = open('../files/tmp_03.txt', 'w', encoding='utf-8')
file3.write(new_content)
file3.close()


file4 = open("../files/tmp_02.txt", "r", encoding="utf-8")
content = file4.read()
file4.close()
file4 = open("../files/tmp_04.txt", "w", encoding="utf-8")
file4.write(content)
file4.close()


file5 = open("../files/tmp_05.txt", "r", encoding="utf-8")
content = file5.read()
file5.close()
file5 = open("../files/tmp_06.txt", "r", encoding="utf-8")
content2 = file5.read()
file5.close()
file5 = open("../files/tmp_07.txt", "w", encoding="utf-8")
file5.write(content + content2)
file5.close()


file6 = open("../files/tmp_08.txt", "r", encoding="utf-8")
line = 1
while True:
    content = file6.readline()
    if line % 2 == 0:
        print(content, end="")
    if not content:
        break
    line += 1
file6.close()
