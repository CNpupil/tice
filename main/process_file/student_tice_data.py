from openpyxl import load_workbook
import pymysql
import sys
from main import tice_tools, models



def init():
    global name_index
    name_index_ch = ['学号', '姓名', '性别', '年级', '身高', '体重', '肺活量', '50m', '跳远', '坐位体前屈', '800m', '1000m', '仰卧起坐', '引体向上', '左眼视力', '右眼视力']
    name_index_en = ['uid', 'name', 'sex', 'grade', 'height', 'weight', 'pulmonary', 'run50', 'jump', 'flextion', 'run800', 'run1000', 'adbominal_curl', 'pull_up', 'left_eye', 'right_eye']
    name_index = { name_index_en[i]: {'name_ch': name_index_ch[i], 'idx': i} for i in range(len(name_index_ch)) }

def read_data_from_excel(filename):
    # 读取xlsx数据
    wb = load_workbook(filename)
    sheets = wb.worksheets
    sheet1 = sheets[0]
    students = []

    for row in sheet1.rows:
        students.append([col.value for col in row])
    del(students[0])
    return students

def preprocess_data(students):
    # validate data
    for student in students:
        student[name_index['uid']] = tice_tools.preprocessing(student[name_index['uid']])
        student[name_index['name']] = tice_tools.preprocessing(student[name_index['name']])
        student[name_index['sex']] = tice_tools.preprocessing(student[name_index['sex']])


def save_data(students, task_id):
    for student in students:
        # validate data
        item = {}
        item['task_id'] = task_id
        item['student_id'] = student[name_index['uid']]
        

        models.StudentInfomation.objects.update_or_create(
            defaults=item,
            student_id = item['student_id'],
            task_id = item['task_id']
        )

def read_student_infomation(task_id, filename):
    students = read_data_from_excel(filename)
    init()
    students = preprocess_data(students)
    save_data(students, task_id)

    