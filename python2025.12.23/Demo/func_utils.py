def process_student_data(data_list, Student, GradeManager):
    """处理学生数据列表"""
    manager = GradeManager()
    
    for item in data_list:
        name = item.get("name")
        student_id = item.get("student_id")
        scores = item.get("scores", {})
        
        if not name or not student_id:
            continue
        
        student = Student(name, student_id)
        
        for subject, score in scores.items():
            try:
                student.add_score(subject, score)
            except ValueError as e:
                print(f"警告: 学生 {name} 的 {subject} 成绩无效: {e}")
                continue
        
        manager.add_student(student)
    
    return manager


def generate_report(manager):
    """生成成绩报告"""
    if not manager.students:
        print("没有学生数据")
        return
    
    print("=" * 50)
    print("学生成绩报告")
    print("=" * 50)
    
    print(f"\n班级平均分: {manager.get_class_average()}")
    
    print("\n等级分布:")
    distribution = manager.get_grade_distribution()
    for grade, count in distribution.items():
        print(f"  {grade}: {count}人")
    
    print("\n前3名优秀学生:")
    top_students = manager.get_top_students(3)
    for i, student in enumerate(top_students, 1):
        print(f"  {i}. {student.name} (学号: {student.student_id}, 平均分: {student.get_average()}, 等级: {student.get_grade()})")
    
    # 统计各科目
    all_subjects = set()
    for student in manager.students:
        all_subjects.update(student.scores.keys())
    
    if all_subjects:
        print("\n各科目统计:")
        for subject in sorted(all_subjects):
            stats = manager.get_subject_statistics(subject)
            if stats:
                print(f"  {subject}:")
                print(f"    最高分: {stats['最高分']}, 最低分: {stats['最低分']}, 平均分: {stats['平均分']}, 参考人数: {stats['人数']}")

