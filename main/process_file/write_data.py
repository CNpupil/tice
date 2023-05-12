import json
import pandas as pd
from tice import settings
from main import tice_tools


def write_data_to_file(data, filename):
    # data = [{"student__uid": "202003551218", "student__name": "冯伟杰", "student__sex": 2, "height": None, "weight": None, "pulmonary": None, "run50": None, "jump": None, "flexion": None, "run800": None, "run1000": None, "adbominal_curl": None, "pull_up": None, "left_eye": None, "right_eye": None}, {"student__uid": "202003551327", "student__name": "陆小玲", "student__sex": 2, "height": 155.0, "weight": None, "pulmonary": None, "run50": None, "jump": None, "flexion": None, "run800": None, "run1000": None, "adbominal_curl": None, "pull_up": None, "left_eye": None, "right_eye": None}]
    projetcts = {
        'student__uid': '学号',
        'student__name': '姓名',
        'student__sex': '性别',
        'height': '身高',
        'weight': '体重',
        'pulmonary': '肺活量',
        'run50': '50m',
        'jump': '跳远',
        'flexion': '坐位体前屈',
        'run800': '800m',
        'run1000': '1000m', 
        'adbominal_curl': '仰卧起坐',
        'pull_up': '引体向上',
        'left_eye': '左眼',
        'right_eye': '右眼',
        'bmi_score': 'BMI得分',
        'pulmonary_score': '肺活量得分',
        'run50_score': '50m得分',
        'jump_score': '跳远得分',
        'flexion_score': '坐位体前屈得分',
        'runlong_score': '800m/1000m得分',
        'curlorup_score': '仰卧起坐/引体向上得分',
        'end_score': '最终得分',
    }
    for item in data:
        if item['student__sex'] == 2 and item.get('run800', 'pp') != 'pp' and item['run800']:
            item['run800'] = tice_tools.int_to_time(item['run800'])
        if item['student__sex'] == 1 and item.get('run1000', 'pp') != 'pp' and item['run1000']:
            item['run1000'] = tice_tools.int_to_time(item['run1000'])
        item['student__sex'] = '男' if item['student__sex'] == 1 else '女'
        for key, value in projetcts.items():
            if item.get(key, 'pp') != 'pp':
                item[value] = item[key]
                del item[key]
    df = pd.DataFrame(data)
    df.to_excel(settings.MEDIA_ROOT +  filename + '.xlsx', index=False, engine='openpyxl')
    return filename + '.xlsx'

