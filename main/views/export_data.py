from rest_framework.views import APIView
from django.core import serializers
from django.http import JsonResponse
from django.db.models import F

from main import models
from main import tools, tice_tools
from main.process_file.write_data import write_data_to_file

import json


class ExportTaskData(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            data = json.loads(request.body).get('data', {})
            task_id = data.get('task_id', -1)
            items = data.get('items', [])

            data = models.Score.objects.filter(task_id=task_id).values(
                * items
            )
            ret['data'] = json.dumps(list(data))

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)
    

class ExportTaskStandardData(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            task_id = request.GET.get('task_id', -1)

            data = models.Score.objects.filter(task_id=task_id).values(
                'student__uid',
                'student__name',
                'student__sex',
                'height',
                'weight',
                'pulmonary',
                'run50',
                'jump',
                'flexion',
                'run800',
                'run1000',
                'adbominal_curl',
                'pull_up',
                'left_eye',
                'right_eye',
            )
            ret['filename'] = write_data_to_file(data, tools.generateString16())
            # ret['data'] = json.dumps(list(data))

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}
            print(str(e))

        return JsonResponse(ret)