from django.db import models


class User(models.Model):
    uid = models.CharField(max_length=50, unique=True, db_index=True, default='null')
    name = models.CharField(max_length=50, default='null')
    password = models.CharField(max_length=50, default='null')
    email = models.CharField(max_length=50, default='null', unique=True, db_index=True,)
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