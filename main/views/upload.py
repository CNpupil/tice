from rest_framework.views import APIView
from django.core import serializers
from django.http import JsonResponse

from main import models
from main import tools

import json

class UploadStudentInfomation(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            file = request.FILES.get('file', None)
            if file is None:
                return JsonResponse({'code': 400, 'msg': '文件不能为空'})
            
            fileObj = models.TempFile.objects.create(file=file)
            # print(fileObj.file)

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)