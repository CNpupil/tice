from openpyxl import load_workbook
import pymysql
import sys
from main import tice_tools, models



def init():
    global name_index
    name_index_ch = ['学号', '姓名', '性别', '身高', '体重', '肺活量', '50m', '坐位体前屈', '跳远', '800m', '1000m', '仰卧起坐', '引体向上', '左眼视力', '右眼视力']
    name_index_en = ['uid', 'name', 'sex', 'height', 'weight', 'pulmonary', 'run50', 'flexion', 'jump', 'run800', 'run1000', 'adbominal_curl', 'pull_up', 'left_eye', 'right_eye']
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
        student[name_index['uid']['idx']] = tice_tools.preprocessing(student[name_index['uid']['idx']])
        student[name_index['name']['idx']] = tice_tools.preprocessing(student[name_index['name']['idx']])
        student[name_index['sex']['idx']] = tice_tools.preprocessing(student[name_index['sex']['idx']])
    return students


def save_data(students, task_id):
    for student in students:
        # validate data
        item = {}
        item['task_id'] = task_id
        item['student_id'] = student[name_index['uid']['idx']]
        for i in name_index.keys():
            item[i] = student[name_index[i]['idx']]
        
        item['sex'] = 1 if student[name_index['sex']['idx']] == '男' else 2
        if item['sex'] == 2:
            item['run800'] = tice_tools.time_to_int(student[name_index['run800']['idx']])
        else:
            item['run1000'] = tice_tools.time_to_int(student[name_index['run1000']['idx']])
        student = models.StudentInfomation.objects.filter(uid=item['student_id']).first()
        item['student_id'] = student.pk
        models.Score.objects.update_or_create(
            defaults = item,
            task_id = item['task_id'],
            student_id = student.pk,
        )
        tice_tools.calc_all_score(task_id, student.pk)

def read_student_score(task_id, filename):
    students = read_data_from_excel(filename)
    init()
    students = preprocess_data(students)
    save_data(students, task_id)

    