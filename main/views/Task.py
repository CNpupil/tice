from rest_framework.views import APIView
from django.core import serializers
from django.http import JsonResponse

from main import models
from main import tools

import json

class Task(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            tasks = models.Task.objects.all().order_by('-pk')
            ret['data'] = serializers.serialize('json', tasks)

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

        return JsonResponse(ret)

    def put(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '修改成功'}
        try:
            data = json.loads(request.body).get('data', {})

            # validate data

            task = models.Task.objects.filter(pk=data.get('task_pk', 0)).first()
            if task is None:
                return JsonResponse({'code': 400, 'msg': '任务不存在'})
            setatter(task, data['key'], data['value'])            

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

