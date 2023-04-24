from django.db import models


class User(models.Model):
    uid = models.CharField(max_length=50, unique=True, db_index=True, default='null')
    name = models.CharField(max_length=50, default='null')
    password = models.CharField(max_length=50, default='null')
    # email = models.CharField(max_length=50, default='null', unique=True, db_index=True,)
    token = models.CharField(max_length=50, default='null')
    auth = models.IntegerField(default=0)
    # 0 loading, 1 normal, 2 delete
    status = models.IntegerField(default=0)


class Token(models.Model):
    value = models.CharField(max_length=50, unique=True, db_index=True, default='null')
    expire_time = models.IntegerField(default=0)
    

class Task(models.Model):
    name = models.TextField(default='')
    begin_time = models.IntegerField(default=0)
    end_time = models.IntegerField(default=0)
    # 0 loading, 1 expire, 2 delete
    status = models.IntegerField(default=0)
    year = models.IntegerField(default=2019)
    half = models.IntegerField(default=0)


class TeacherInfomation(models.Model):
    uid = models.CharField(max_length=50, unique=True, db_index=True, default='null')
    name = models.CharField(max_length=30, default='')


class StudentInfomation(models.Model):
    uid = models.CharField(max_length=50, unique=True, db_index=True, default='null')
    college = models.CharField(max_length=30, default='')
    grade = models.IntegerField(default=2019)
    major = models.CharField(max_length=50, default='')
    class_name = models.IntegerField(default=1)
    name = models.CharField(max_length=30, default='')
    sex = models.IntegerField(default=0)
    brithday = models.IntegerField(default=0)
    source = models.CharField(max_length=30, default='')
    address = models.TextField(default='')
    idcard = models.CharField(max_length=19, default='')
    nation = models.CharField(max_length=19, default='')


class Score(models.Model):
    task = models.ForeignKey("main.Task", models.CASCADE)
    student = models.ForeignKey("main.StudentInfomation", models.CASCADE)
    height = models.DecimalField(max_digits=6, decimal_places=2, default=160, null=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, default=50, null=True)
    pulmonary = models.IntegerField(default=2000, null=True)
    run50 = models.DecimalField(max_digits=6, decimal_places=2, default=10, null=True)
    jump = models.DecimalField(max_digits=6, decimal_places=2, default=180, null=True)
    flexion = models.DecimalField(max_digits=6, decimal_places=2, default=10, null=True)
    run800 = models.IntegerField(default=0, null=True)
    run1000 = models.IntegerField(default=0, null=True)
    adbominal_curl = models.IntegerField(default=30, null=True)
    pull_up = models.IntegerField(default=5, null=True)
    left_eye = models.DecimalField(max_digits=6, decimal_places=2, default=5, null=True)
    right_eye = models.DecimalField(max_digits=6, decimal_places=2, default=5, null=True)

    bmi_score = models.IntegerField(default=65, null=True)
    pulmonary_score = models.IntegerField(default=65, null=True)
    run50_score = models.IntegerField(default=65, null=True)
    jump_score = models.IntegerField(default=65, null=True)
    flexion_score = models.IntegerField(default=65, null=True)
    runlong_score = models.IntegerField(default=65, null=True)
    curlorup_score = models.IntegerField(default=65, null=True)
    end_score = models.IntegerField(default=65, null=True)
    remark = models.TextField(default='')


class ScoreStandard(models.Model):
    grade = models.TextField(default='low')
    bmi = models.TextField(default='[]')
    pulmonary = models.TextField(default='[]')
    run50 = models.TextField(default='[]')
    jump = models.TextField(default='[]')
    flexion = models.TextField(default='[]')
    run800 = models.TextField(default='[]')
    run1000 = models.TextField(default='[]')
    adbominal_curl = models.TextField(default='[]')
    pull_up = models.TextField(default='[]')
    run1000 = models.TextField(default='[]')
    end_score = models.TextField(default='[]')


class ClassInfomation(models.Model):
    grade = models.TextField(default='未知')
    college = models.TextField(default='未知')
    major = models.TextField(default='未知')
    class_id = models.TextField(default='')


class TempFile(models.Model):
    file = models.FileField(upload_to='temp/', max_length=100)