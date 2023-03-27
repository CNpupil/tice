from rest_framework.views import APIView
from django.core import serializers
from django.http import JsonResponse

from main import models

import json

class User(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            users = models.User.objects.all().order_by('pk')

            ret['data']  = serializers.serialize('json', users)

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)

    def put(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '修改成功'}
        try:
            data = json.loads(request.body).get('data', {})

            # validate data

            user = models.User.objects.filter(uid=data.get('uid', '')).first()
            if user is None:
                return JsonResponse({'code': 400, 'msg': '用户不存在'})
            setatter(user, data['key'], data['value'])

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)


class ChangePassword(APIView):
    def put(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}  
        try:
            data = json.loads(request.body).get('data', {})

            # validate data

            user = models.User.objects.filter(uid=data.get('uid', '')).first()
            if user is None:
                return JsonResponse({'code': 400, 'msg': '用户不存在'})
            user.password = tools.generateMD5(data['password'])
            user.save()

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)


class Register(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '登录成功'}
        try:
            data = json.loads(request.body).get('data', {})

            # validate data

            data['password'] = tools.generateMD5(data['password'])

            user = models.User.create(
                uid = data['uid'],
                password = data['password'],
                token = tools.generateString16(),
                auth = data['uid'],
                status = 0,
            )

            ret['data'] = serializers.serialize('json', user)

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)

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