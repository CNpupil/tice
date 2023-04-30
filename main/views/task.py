from rest_framework.views import APIView
from django.core import serializers
from django.http import JsonResponse

from main import models
from main import tools

import json
import math


class Task(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            task_id = request.GET.get('task_id', -1)
            task = models.Task.objects.filter(pk=task_id)
            ret['data'] = serializers.serialize('json', task)   

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)

    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '添加成功'}
        try:
            data = json.loads(request.body).get('data', {})

            # validate data

            models.Task.objects.create(
                name = data['name'],
                begin_time = data['begin_time'],
                end_time = data['end_time'],
                status = 0,
                year = data['year'],
                half = data['half'],
            )            

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}
            ret = {'code': 500, 'msg': 'Timeout', 'error': str(e)}

        return JsonResponse(ret)

    def put(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '修改成功'}
        try:
            data = json.loads(request.body).get('data', {})

            if None in [data.get('key', None), data.get('value', None)]:
                return JsonResponse({'code': 400, 'msg': '参数错误'})

            task = models.Task.objects.filter(pk=data.get('task_pk', 0)).first()
            if task is None:
                return JsonResponse({'code': 400, 'msg': '任务不存在'})
            setattr(task, data['key'], data['value']) 
            task.save()           

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)

    def delete(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '删除成功'}
        try:
            data = json.loads(request.body).get('data', {})

            # validate data

            task = models.Task.objects.filter(pk=data.get('task_pk', 0)).first()
            if task is None:
                return JsonResponse({'code': 400, 'msg': '任务不存在'})
            task.delete()        

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)


class TaskList(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            tasks = models.Task.objects.all().order_by('-pk')
            ret['data'] = serializers.serialize('json', tasks)

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)


class DistributeTeacher(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '分配成功'}
        try:
            data = json.loads(request.body).get('data', {})
            task_id = data.get('task_id', 0)
            teacher_list = data.get('teachers', [])

            # validate data

            scores = models.Score.objects.filter(task_id=task_id).order_by('student__college', 'student__major', 'student__class_name')
            student_count = scores.count()
            member_count = math.ceil(student_count / len(teacher_list))

            pks = []
            for score in scores:
                pks.append(score.pk)

            begin, end = 0, member_count
            for teacher in teacher_list:
                models.Score.objects.filter(pk__in=pks[begin:end]).update(teacher_id=teacher)
                begin, end = end, min(end + member_count, len(scores))


        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}
            ret = {'code': 500, 'msg': 'Timeout', 'error': str(e)}

        return JsonResponse(ret)
    

class TaskByTeacher(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '分配成功'}
        try:
            teacher_id = request.GET.get('teacher_id', -1)

            task_list = list(set(models.Score.Objects.filter(teacher_id=teacher_id).values('task_id')))

            data = models.Task.objects.filter(pk__in=task_list)
            ret['data'] = serializers.serialize('json', data)

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)
    

class StudentFromTaskByTeacher(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '分配成功'}
        try:
            teacher_id = request.GET.get('teacher_id', -1)
            task_id = request.GET.get('task_id', -1)

            data = models.Score.objects.filter(
                task_id = task_id,
                teacher_id = teacher_id
            ).order_by('student_id')

            ret['data'] = serializers.serialize('json', data, use_natural_foreign_keys=True)

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)

    def put(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '保存成功'}
        try:
            data = json.loads(request.body).get('data', {})
            task_id = data.get('task_id', -1)
            teacher_id = data.get('teacher_id', -1)
            score_list = data.get('score_list', [])

            for score in score_list:
                models.Score.objects.filter(task_id=task_id, teacher_id=teacher_id, student_id=score['student_id']).update(
                    **score
                )

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)

