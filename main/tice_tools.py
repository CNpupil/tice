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

# grading = [
#     {'value': 100, 'score': 100}, 
#     {'value': 80, 'score': 80}, 
#     {'value': 70, 'score': 70}, 
#     {'value': 0, 'score': 10}
# ]
def calc_item_score(value, grading, order=True):
    for t in grading:
        res = value >= t['value'] if order else value <= t['value']
        if res:
            return t['score']
    return 0

scores = [{'name': 88}, ]
weights = {'bmi': 0.15, 'pulmonary': 0.15, 'run50': 0.2, 'jump': 0.1, 'flexion': 0.1, 'runlong': 0.2, 'curlorup': 0.1}
def calc_end_score(scores, weights):
    end_score = sum([(getattr(scores, key+'_score') if getattr(scores, key+'_score') else 0) * weights[key] for key in weights.keys()])
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
        if score >= t['value']:
            return t['name']
    return False

def calc_tags_count(scores):
    tags = {'excellent': 0, 'good': 0, 'qualified': 0, 'unqualified': 0}
    for score in scores:
        score = score if score else 0
        grade_name = calc_tag(score)
        tags[grade_name] = tags.get(grade_name, 0) + 1
    return tags

def calc_grade(year, half, grade):
    if (year - grade) <= 2 and half == 1:
        return 'low'
    return 'high'



from main.models import ScoreStandard, Score, StudentInfomation, Task
import json


class CalcScore:
    def __init__(self, grade='low', sex='male'):
        score_standard = ScoreStandard.objects.filter(grade=grade).first()
        self.bmi_standard = json.loads(score_standard.bmi)[sex]
        self.pulmonary_standard = json.loads(score_standard.pulmonary)[sex]
        self.run50_standard = json.loads(score_standard.run50)[sex]
        self.jump_standard = json.loads(score_standard.jump)[sex]
        self.flexion_standard = json.loads(score_standard.flexion)[sex]
        self.run800_standard = json.loads(score_standard.run800)[sex]
        self.run1000_standard = json.loads(score_standard.run1000)[sex]
        self.adbominal_curl_standard = json.loads(score_standard.adbominal_curl)[sex]
        self.pull_up_standard = json.loads(score_standard.pull_up)[sex]
        self.end_score_standard = json.loads(score_standard.end_score)

    def calc_bmi_score(self, value):
        self.bmi_score = calc_item_score(value, self.bmi_standard)
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
    
    def calc_item_score(self, key, value):
        score = getattr(self, 'calc_{}_score'.format(key))(value)
        return score

    def calc_all_score(self, data, keys=[]):
        for key in keys:
            self.calc_item_score(key, data[key])
    
    
def calc_all_score(task_id, student_id):
    score = Score.objects.filter(task_id=task_id, student_id=student_id).first()
    task = Task.objects.filter(pk=task_id).first()
    student = StudentInfomation.objects.filter(pk=student_id).first()

    calc_score = CalcScore(
        grade=calc_grade(task.year, task.half, student.grade),
        sex='male' if student.sex == 1 else 'female'
    )
    
    if score.height != None and score.weight != None:
        score.bmi_score = calc_score.calc_bmi_score(score.weight / ((score.height / 100) ** 2))
    if score.pulmonary:
        score.pulmonary_score = calc_score.calc_pulmonary_score(score.pulmonary)
    if score.flexion:
        score.flexion_score = calc_score.calc_flexion_score(score.flexion)
    if score.jump:
        score.jump_score = calc_score.calc_jump_score(score.jump)
    if score.run50:
        score.run50_score = calc_score.calc_run50_score(score.run50)
    if score.run800 and student.sex == 2:
        score.runlong_score = calc_score.calc_run800_score(score.run800)
    if score.run1000 and student.sex == 1:
        score.runlong_score = calc_score.calc_run1000_score(score.run1000)
    if score.adbominal_curl and student.sex == 2:
        score.curlorup_score = calc_score.calc_adbominal_curl_score(score.adbominal_curl)
    if score.pull_up and student.sex == 1:
        score.curlorup_score = calc_score.calc_pull_up_score(score.pull_up)
    score.end_score = calc_score.calc_end_score(score)

    score.save()