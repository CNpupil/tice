from openpyxl import load_workbook
import pymysql
import sys
from main import tice_tools, models



def init():
    global name_index
    name_index_ch = ['学号', '姓名', '性别', '年级', '院系', '专业', '行政班级', '身份证号', '学生来源代码', '家庭住址', '民族代码']
    name_index_en = ['uid', 'name', 'sex', 'grade', 'college', 'major', 'class_name', 'idcard', 'source', 'address', 'nation']
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
        student[name_index['college']['idx']] = tice_tools.preprocessing(student[name_index['college']['idx']])
        student[name_index['major']['idx']] = tice_tools.preprocessing(student[name_index['major']['idx']])
        student[name_index['class_name']['idx']] = tice_tools.preprocessing(student[name_index['class_name']['idx']])
        student[name_index['idcard']['idx']] = tice_tools.preprocessing(student[name_index['idcard']['idx']])
        student[name_index['source']['idx']] = tice_tools.preprocessing(student[name_index['source']['idx']])
        student[name_index['address']['idx']] = tice_tools.preprocessing(student[name_index['address']['idx']])
        student[name_index['nation']['idx']] = tice_tools.preprocessing(student[name_index['nation']['idx']])
        student[name_index['grade']['idx']] = tice_tools.preprocessing(student[name_index['grade']['idx']])
        student[name_index['grade']['idx']] = tice_tools.convert_to_int(student[name_index['grade']['idx']])
    return students

def save_data(students):
    for student in students:
        # validate data
        item = {}
        item['uid'] = student[name_index['uid']['idx']]
        item['name'] = student[name_index['name']['idx']]
        item['sex'] = 1 if student[name_index['name']['idx']] == '男' else '女'
        item['grade'] = student[name_index['grade']['idx']]
        item['college'] = student[name_index['college']['idx']]
        item['major'] = student[name_index['major']['idx']]
        item['class_name'] = student[name_index['class_name']['idx']]
        item['idcard'] = student[name_index['idcard']['idx']]
        # 转换为相应代码
        item['source'] = student[name_index['source']['idx']]
        item['address'] = student[name_index['address']['idx']]
        # 转换为相应代码
        item['nation'] = student[name_index['nation']['idx']]
        # convert to timestamp
        item['brithday'] = tice_tools.birthday_to_timestamp(item['idcard'][6:14])

        models.StudentInfomation.objects.update_or_create(
            defaults=item,
            uid = item['uid']
        )

def read_student_infomation(task_id, filename):
    students = read_data_from_excel(filename)
    init()
    students = preprocess_data(students)
    save_data(students)

    