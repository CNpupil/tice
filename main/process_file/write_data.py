import json
import pandas as pd
from tice import settings


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
    }
    for item in data:
        for key, value in projetcts.items():
            if item.get(key, 'pp') != 'pp':
                print(key)
                item[value] = item[key]
                del item[key]
    print(data)
    df = pd.DataFrame(data)
    df.to_excel(settings.MEDIA_ROOT +  filename + '.xlsx', index=False, engine='openpyxl')
    return filename + '.xlsx'

