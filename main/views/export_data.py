from rest_framework.views import APIView
from django.core import serializers
from django.http import JsonResponse

from main import models
from main import tools, tice_tools

import json

class ExportTaskData(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            task_id = request.GET.get('task_id', -1)
            task = models.Task.objects.filter(pk=task_id).first()
            if task is None:
                return JsonResponse({'code': 400, 'msg': '该任务不存在'})
            score = models.Score.objects.filter(task_id=task_id)
            ret['data'] = serializers.serialize('json', score, use_natural_foreign_keys=True)

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)