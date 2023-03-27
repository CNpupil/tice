from django.http import JsonResponse
from django.core import serializers
from rest_framework.views import APIView

from main import models
from main import tools

import json


class Login(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '登录成功'}
        try:
            data = json.loads(request.body).get('data', {})

            uid = data.get('uid', '')
            password = data.get('password', '')
            if uid == '' or password == '':
                return JsonResponse({'code': 400, 'msg': '用户名或密码错误'})
            
            user = models.User.objects.filter(uid=uid).first()
            if user is None:
                return JsonResponse({'code': 400, 'msg': '用户名或密码错误'})
            
            if tools.genearteMD5(password) != user.password:
                return JsonResponse({'code': 400, 'msg': '用户名或密码错误'})

            ret['data'] = serializers.serialize('json', user)

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)