from rest_framework.views import APIView
from django.core import serializers
from django.http import JsonResponse

from main import models
from main import tools
from main.process_file import student_tice_data, student_basic_infomation
from tice import settings

import json

class UploadStudentInfomation(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            task_id = request.POST.get('task_id', -1)
            file = request.FILES.get('file', None)
            if file is None:
                return JsonResponse({'code': 400, 'msg': '文件不能为空'})
            
            fileObj = models.TempFile.objects.create(file=file)

            student_basic_infomation.read_student_infomation(task_id, settings.MEDIA_ROOT + fileObj.file.name)
            models.Task.objects.filter(pk=task_id).update(status=2)
            # print(fileObj.file)

        except Exception as e:
            if str(e)[:3] == 'ppp':
                ret = {'code': 500, 'msg': str(e).replace('ppp', '')}
            else:
                ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)


class UploadStudentScore(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            task_id = request.POST.get('task_id', -1)
            file = request.FILES.get('file', None)
            if file is None:
                return JsonResponse({'code': 400, 'msg': '文件不能为空'})
            
            fileObj = models.TempFile.objects.create(file=file)

            student_tice_data.read_student_score(task_id, settings.MEDIA_ROOT + fileObj.file.name)
            # print(fileObj.file)

        except Exception as e:
            # print(str(e))
            if str(e)[:3] == 'ppp':
                ret = {'code': 500, 'msg': str(e).replace('ppp', '')}
            else:
                ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)