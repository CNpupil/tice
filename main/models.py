from django.db import models


class User(models.Model):
    uid = models.CharField(max_length=50, unique=True, db_index=True, default='null')
    name = models.CharField(max_length=50, default='null')
    password = models.CharField(max_length=50, default='null')
    # email = models.CharField(max_length=50, default='null', unique=True, db_index=True,)
    token = models.TextField(default='null')
    auth = models.IntegerField(default=0)
    # 0 loading, 1 normal, 2 delete
    status = models.IntegerField(default=0)

    def natural_key(self):
        return {'name': self.name, 'auth': self.name, 'status': self.status}


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

    def natural_key(self):
        return {'name': self.name, 'year': self.year, 'half': self.half}


class TeacherInfomation(models.Model):
    user = models.OneToOneField("main.User", on_delete=models.CASCADE)
    uid = models.CharField(max_length=50, unique=True, db_index=True, default='null')
    name = models.CharField(max_length=30, default='')

    def natural_key(self):
        return {'uid': self.uid, 'name': self.name}


class StudentInfomation(models.Model):
    user = models.OneToOneField("main.User", on_delete=models.CASCADE)
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

    def natural_key(self):
        data = {}
        data['pk'] = self.id
        data['uid'] = self.uid
        data['college'] = self.college
        data['grade'] = self.grade
        data['major'] = self.major
        data['class_name'] = self.class_name
        data['name'] = self.name
        data['sex'] = self.sex
        data['brithday'] = self.brithday
        data['source'] = self.source
        data['address'] = self.address
        data['idcard'] = self.idcard
        data['nation'] = self.nation
        return data


class Score(models.Model):
    task = models.ForeignKey("main.Task", models.CASCADE)
    student = models.ForeignKey("main.StudentInfomation", models.CASCADE)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    pulmonary = models.IntegerField(null=True)
    run50 = models.FloatField(null=True)
    jump = models.FloatField(null=True)
    flexion = models.FloatField(null=True)
    run800 = models.IntegerField(null=True)
    run1000 = models.IntegerField(null=True)
    adbominal_curl = models.IntegerField(null=True)
    pull_up = models.IntegerField(null=True)
    left_eye = models.FloatField(null=True)
    right_eye = models.FloatField(null=True)

    bmi_score = models.IntegerField(null=True)
    pulmonary_score = models.IntegerField(null=True)
    run50_score = models.IntegerField(null=True)
    jump_score = models.IntegerField(null=True)
    flexion_score = models.IntegerField(null=True)
    runlong_score = models.IntegerField(null=True)
    curlorup_score = models.IntegerField(null=True)
    end_score = models.IntegerField(null=True)
    teacher = models.ForeignKey("main.TeacherInfomation", models.CASCADE, null=True, blank=True)
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
    end_score = models.TextField(default='[]')


class ClassInfomation(models.Model):
    grade = models.TextField(default='未知')
    college = models.TextField(default='未知')
    major = models.TextField(default='未知')
    class_id = models.TextField(default='')


class TempFile(models.Model):
    file = models.FileField(upload_to='temp/', max_length=100)


# null


# class Category(models.Model):
#     # netflix / apple music / chatgpt
#     type_name = models.CharField(max_length=20, default='', verbose_name='类别')
#     name = models.TextField(default='', verbose_name='类别名称')
#     sum_seat = models.IntegerField(default=5, verbose_name='最大人数')
#     year_price = models.FloatField(default=1, verbose_name='年费用')
#     quarter_price = models.FloatField(default=1, verbose_name='季度费用')
#     month_price = models.FloatField(default=1, verbose_name='月费用')
#     day_price = models.FloatField(default=1, verbose_name='日费用')

#     def __str__(self):
#         return self.name
    

# class Warehouse(models.Model):
#     info = models.ForeignKey("main.Category", on_delete=models.CASCADE, verbose_name='类别')
#     username = models.TextField(default='', verbose_name='账号')
#     password = models.TextField(default='', verbose_name='密码')
#     expired_time = models.DateTimeField(default=0, verbose_name='过期时间')
#     register_email = models.TextField(default='', verbose_name='注册邮箱')

#     def __str__(self):
#         return self.username
    

# class account(models.Model):
#     warehouse = models.ForeignKey("main.Warehouse", on_delete=models.CASCADE, verbose_name='房主')
#     # 0：not initialized 1: use 2: use over
#     status = models.IntegerField(default=0, berbose_name='状态')
#     expired_time = models.DateTimeField(default=0, verbose_name='过期时间')
#     price = models.FloatField(default=0, verbose_name='价格')

#     def __str__(self):
#         return self.status
    

# class PureAccount(models.Model):
#     username = models.TextField(default='', verbose_name='账号')
#     password = models.TextField(default='', verbose_name='密码')
#     register_email = models.TextField(default='', verbose_name='注册邮箱')
#     type_name = models.TextField(default='', verbose_name='类型')
#     # 0： use 1: use over
#     status = models.IntegerField(default='', verbose_name='状态')

#     def __str__(self):
#         return self.username
    