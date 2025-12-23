score1 = int(input("请输入第一科成绩："))
score2 = int(input("请输入第二科成绩："))
score3 = int(input("请输入第三科成绩："))

if score1 >= score2 and score1 >= score3:
    max_score = score1
elif score2 >= score1 and score2 >= score3:
    max_score = score2
else:
    max_score = score3

if score1 <= score2 and score1 <= score3:
    min_score = score1
elif score2 <= score1 and score2 <= score3:
    min_score = score2
else:
    min_score = score3

average_score = (score1 + score2 + score3) / 3

print(f"最高分：{max_score}")
print(f"最低分：{min_score}")
print(f"平均分：{average_score:.2f}")

