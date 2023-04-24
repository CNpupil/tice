from datetime import datetime


def preprocessing(value):
    value = str(value)
    value = value.strip()
    return value

def check_is_number(value):
    try:
        value = int(value)
        return True
    except Exception as e:
        return False

def convert_to_int(value):
    return int(value)

def convert_to_float(value, decimal=2):
    value = float(value)
    value = round(value, decimal)
    return value

def time_to_int(value):
    a, b = map(int, str(value).split("'"))
    return a * 60 + b

def int_to_time(value):
    a, b = value // 60, value % 60
    return "{}'{}".format(a, b)

def birthday_to_timestamp(value):
    date_obj = datetime.strptime(value, '%Y%m%d')
    timestamp = datetime.timestamp(date_obj)   
    return timestamp 

grading = [
    {'value': 100, 'score': 100}, 
    {'value': 80, 'score': 80}, 
    {'value': 70, 'score': 70}, 
    {'value': 0, 'score': 10}
]
def calc_item_score(value, grading, order=True):
    for t in grading:
        res = value >= t.value if order else value <= t.value
        if res:
            return t.score
    return 0

scores = [{'name': 88}, ]
weights = [{'bmi': 0.2}, ]
def calc_end_score(scores, weights):
    end_score = sum([scores[key] * weights[key] for key in scores.keys()])
    return end_score

scores = [99, 22]
def calc_tag(score):
    standard_tag = [
        { 'value': 90, 'name': 'excellent' },
        { 'value': 80, 'name': 'good' },
        { 'value': 60, 'name': 'qualified' },
        { 'value': 0, 'name': 'unqualified' },
    ]
    for t in standard_tag:
        if score >= t.value:
            return t.name
    return False

def calc_tags_count(scores):
    tags = {}
    for score in scores:
        grade_name = calc_tag(score)
        tags[grade_name] = tags.get(grade_name, 0) + 1
    return tags



from main import models
import json


class CalcScore:
    def __init__(self, grade='low'):
        score_standard = models.ScoreStandard.objects.filter(grade=grade).first()
        self.bmi_standard = json.loads(score_standard.bmi)
        self.pulmonary_standard = json.loads(score_standard.pulmonary)
        self.run50_standard = json.loads(score_standard.run50)
        self.jump_standard = json.loads(score_standard.jump)
        self.flexion_standard = json.loads(score_standard.flexion)
        self.run800_standard = json.loads(score_standard.run800)
        self.run1000_standard = json.loads(score_standard.run1000)
        self.adbominal_curl_standard = json.loads(score_standard.adbominal_curl)
        self.pull_up_standard = json.loads(score_standard.pull_up)
        self.run1000_standard = json.loads(score_standard.run1000)
        self.end_score_standard = json.loads(score_standard.end_score)

    # bmi需要特殊处理
    def calc_bmi_score(self, value):
        self.bmi_score  = calc_item_score(value, self.bmi_standard)
        return self.bmi_score

    def calc_pulmonary_score(self, value):
        self.pulmonary_score = calc_item_score(value, self.pulmonary_standard)
        return self.pulmonary_score

    def calc_run50_score(self, value):
        self.run50_score = calc_item_score(value, self.run50_standard, order=False)
        return self.run50_score

    def calc_jump_score(self, value):
        self.jump_score = calc_item_score(value, self.jump_standard)
        return self.jump_score

    def calc_flexion_score(self, value):
        self.flexion_score = calc_item_score(value, self.flexion_standard)
        return self.flexion_score

    def calc_run800_score(self, value):
        self.run800_score = calc_item_score(value, self.run800_standard, order=False)
        return self.run800_score

    def calc_run1000_score(self, value):
        self.run1000_score = calc_item_score(value, self.run1000_standard, order=False)
        return self.run1000_score

    def calc_adbominal_curl_score(self, value):
        self.adbominal_curl_score = calc_item_score(value, self.adbominal_curl_standard)
        return self.adbominal_curl_score

    def calc_pull_up_score(self, value):
        self.pull_up_score = calc_item_score(value, self.pull_up_standard)
        return self.pull_up_score

    def calc_end_score(self, value):
        self.end_score = calc_end_score(value, self.end_score_standard)
        return self.end_score
    
    
    
