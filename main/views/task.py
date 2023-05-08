from rest_framework.views import APIView
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Count, Q

from main import models
from main import tools, tice_tools

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
                status = 3,
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

            task_id = data.get('task_id')
            task = models.Task.objects.filter(pk=task_id)
            if task.count() == 0:
                return JsonResponse({'code': 400, 'msg': '该任务不存在'})
            
            task.update(
                name = data.get('name', ''),
                begin_time = data.get('begin_time', 0),
                end_time = data.get('end_time', 0),
                year = data.get('year', 1977),
                half = data.get('half', 0),
            )

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

            models.Task.objects.filter(pk=task_id).update(status=1)


        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}
            ret = {'code': 500, 'msg': 'Timeout', 'error': str(e)}

        return JsonResponse(ret)
    

class TaskByTeacher(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            teacher_id = request.GET.get('teacher_id', -1)

            task_list = [t['task_id'] for t in models.Score.objects.filter(teacher_id=teacher_id).values('task_id')]

            print(task_list)

            data = models.Task.objects.filter(pk__in=task_list)
            ret['data'] = serializers.serialize('json', data)

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}
            ret = {'code': 500, 'msg': 'Timeout', 'error': str(e)}

        return JsonResponse(ret)
    

class StudentFromTaskByTeacher(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            teacher_id = request.GET.get('teacher_id', -1)
            task_id = request.GET.get('task_id', -1)
            search_key = request.GET.get('search_key', None)
            search_value = request.GET.get('search_value', None)
            grade = request.GET.get('grade', None)
            college = request.GET.get('college', None)
            major = request.GET.get('major', None)
            class_name = request.GET.get('class_name', None)

            data = models.Score.objects.filter(
                task_id = task_id,
                teacher_id = teacher_id,
                student__grade = grade,
                student__college = college,
                student__major = major,
                student__class_name = class_name,
            ).order_by('student_id')
            if search_key:
                search_key += '__icontains'
                data = data.filter(**{search_key:search_value})

            data, ret['page_count'] = tools.myPaginator(data, 20, request.GET.get('page_num', 1))

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
                tice_tools.calc_all_score(task_id, score['student_id'])


        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}
            ret = {'code': 500, 'msg': 'Timeout', 'error': str(e)}

        return JsonResponse(ret)


class TaskProgress(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            task_id = request.GET.get('task_id', -1)

            data = models.Score.objects.values('teacher__name').annotate(
                already_count=Count('end_score', filter=~Q(end_score=None)),
                total_count=Count('id')
            )   
            ret['data'] = json.dumps(list(data))

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}
            print(str(e))

        return JsonResponse(ret)