from func_utils import process_student_data, generate_report


class Student:
    """学生类"""
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.scores = {}
    
    def add_score(self, subject, score):
        """添加科目成绩"""
        if not isinstance(score, (int, float)):
            raise ValueError("成绩必须是数字")
        if score < 0 or score > 100:
            raise ValueError("成绩必须在0-100之间")
        self.scores[subject] = score
    
    def get_average(self):
        """计算平均分"""
        if not self.scores:
            return 0.0
        total = sum(self.scores.values())
        return round(total / len(self.scores), 2)
    
    def get_grade(self):
        """根据平均分获取等级"""
        avg = self.get_average()
        if avg >= 90:
            return "优秀"
        elif avg >= 80:
            return "良好"
        elif avg >= 70:
            return "中等"
        elif avg >= 60:
            return "及格"
        else:
            return "不及格"


class GradeManager:
    """成绩管理器"""
    def __init__(self):
        self.students = []
    
    def add_student(self, student):
        """添加学生"""
        if not isinstance(student, Student):
            raise TypeError("必须是Student对象")
        self.students.append(student)
    
    def find_student_by_id(self, student_id):
        """根据学号查找学生"""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None
    
    def get_class_average(self):
        """计算班级平均分"""
        if not self.students:
            return 0.0
        total_avg = 0
        count = 0
        for student in self.students:
            avg = student.get_average()
            if avg > 0:
                total_avg += avg
                count += 1
        return round(total_avg / count, 2) if count > 0 else 0.0
    
    def get_top_students(self, n=3):
        """获取前n名优秀学生"""
        if not self.students:
            return []
        sorted_students = sorted(
            self.students,
            key=lambda s: s.get_average(),
            reverse=True
        )
        return sorted_students[:n]
    
    def get_grade_distribution(self):
        """统计等级分布"""
        distribution = {
            "优秀": 0,
            "良好": 0,
            "中等": 0,
            "及格": 0,
            "不及格": 0
        }
        for student in self.students:
            grade = student.get_grade()
            if grade in distribution:
                distribution[grade] += 1
        return distribution
    
    def get_subject_statistics(self, subject):
        """获取某科目的统计信息"""
        scores = []
        for student in self.students:
            if subject in student.scores:
                scores.append(student.scores[subject])
        
        if not scores:
            return None
        
        return {
            "最高分": max(scores),
            "最低分": min(scores),
            "平均分": round(sum(scores) / len(scores), 2),
            "人数": len(scores)
        }


# 主程序示例
if __name__ == "__main__":
    # 示例数据
    student_data = [
        {
            "name": "张三",
            "student_id": "2024001",
            "scores": {
                "数学": 95,
                "语文": 88,
                "英语": 92,
                "物理": 90
            }
        },
        {
            "name": "李四",
            "student_id": "2024002",
            "scores": {
                "数学": 85,
                "语文": 82,
                "英语": 78,
                "物理": 88
            }
        },
        {
            "name": "王五",
            "student_id": "2024003",
            "scores": {
                "数学": 75,
                "语文": 70,
                "英语": 72,
                "物理": 68
            }
        },
        {
            "name": "赵六",
            "student_id": "2024004",
            "scores": {
                "数学": 65,
                "语文": 62,
                "英语": 58,
                "物理": 60
            }
        },
        {
            "name": "孙七",
            "student_id": "2024005",
            "scores": {
                "数学": 55,
                "语文": 50,
                "英语": 48,
                "物理": 52
            }
        }
    ]
    
    # 处理数据并生成报告
    grade_manager = process_student_data(student_data, Student, GradeManager)
    generate_report(grade_manager)
    
    # 示例：查找特定学生
    print("\n" + "=" * 50)
    student = grade_manager.find_student_by_id("2024001")
    if student:
        print(f"查找学生: {student.name}")
        print(f"各科成绩: {student.scores}")
        print(f"平均分: {student.get_average()}")
        print(f"等级: {student.get_grade()}")
