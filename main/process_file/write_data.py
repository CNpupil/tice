import json
import pandas as pd
from tice import settings


def write_data_to_file(data, filename):
    # data = [{"student__uid": "202003551218", "student__name": "冯伟杰", "student__sex": 2, "height": None, "weight": None, "pulmonary": None, "run50": None, "jump": None, "flexion": None, "run800": None, "run1000": None, "adbominal_curl": None, "pull_up": None, "left_eye": None, "right_eye": None}, {"student__uid": "202003551327", "student__name": "陆小玲", "student__sex": 2, "height": 155.0, "weight": None, "pulmonary": None, "run50": None, "jump": None, "flexion": None, "run800": None, "run1000": None, "adbominal_curl": None, "pull_up": None, "left_eye": None, "right_eye": None}]
    df = pd.DataFrame(data)
    df.to_excel(settings.MEDIA_ROOT +  filename + '.xlsx', index=False, engine='openpyxl')
    return filename + '.xlsx'

