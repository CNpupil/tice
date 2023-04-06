from rest_framework.views import APIView
from django.core import serializers
from django.http import JsonResponse
from django.core.cache import cache

from main import models
from main import tools
from tice import settings

import json
import jwt


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

            validate = tools.Validate()
            validate.addCheck('isNotEmpty', data.get('uid', None), '用户名不能为空')
            validate.addCheck('isNotEmpty', data.get('key', None), '修改关键字不能为空')
            validate.addCheck('isNotEmpty', data.get('value', None), '修改值不能为空')
            ok, msg = validate.startCheck()
            if not ok:
                return JsonResponse({'code': 400, 'msg': msg})

            user = models.User.objects.filter(uid=data.get('uid', '')).first()
            if user is None:
                return JsonResponse({'code': 400, 'msg': '用户不存在'})
            setattr(user, data['key'], data['value'])

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}
            ret = {'code': 500, 'msg': str(e)}

        return JsonResponse(ret)


class ChangePassword(APIView):
    def put(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '修改成功'}  
        try:
            data = json.loads(request.body).get('data', {})

            validate = tools.Validate()
            validate.addCheck('isNotEmpty', data.get('uid', None), '用户名不能为空')
            validate.addCheck('isNotEmpty', data.get('password', None), '密码不能为空')
            validate.addCheck('checkMaxLength', data.get('password', None), '密码最小长度为5')
            validate.addCheck('checkMinLength', data.get('password', None), '密码最大长度为12')
            ok, msg = validate.startCheck()
            if not ok:
                return JsonResponse({'code': 400, 'msg': msg})

            user = models.User.objects.filter(uid=data.get('uid', '')).first()
            if user is None:
                return JsonResponse({'code': 400, 'msg': '用户不存在'})
            
            user.password = tools.genearteMD5(data['password'])
            user.save()

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)


class Register(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '注册成功'}
        try:
            data = json.loads(request.body).get('data', {})

            validate = tools.Validate()
            validate.addCheck('isNotEmpty', data.get('uid', None), '用户名不能为空')
            validate.addCheck('isNotEmpty', data.get('name', None), '姓名不能为空')
            validate.addCheck('isNotEmpty', data.get('password', None), '密码不能为空')
            validate.addCheck('checkMaxLength', data.get('password', None), '密码最小长度为5')
            validate.addCheck('checkMinLength', data.get('password', None), '密码最大长度为12')
            ok, msg = validate.startCheck()
            if not ok:
                return JsonResponse({'code': 400, 'msg': msg})
            if models.User.objects.filter(uid=data['uid']):
                return JsonResponse({'code': 400, 'msg': '用户名重复'})
                

            data['password'] = tools.genearteMD5(data['password'])

            user = models.User.objects.create(
                uid = data['uid'],
                name = data['name'],
                password = data['password'],
                token = tools.generateString16(),
                auth = 0,
                status = 0,
            )

            ret['data'] = serializers.serialize('json', [user])

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}
            ret = {'code': 500, 'msg': str(e)}

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

            payload = {
                'uid': user.id,
                'auth': user.auth,
            }
            user.token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
            user.save()

            cache.set(user.token, tools.getNowTimeStamp() + settings.JWT_EXPIRATION_DELTA, timeout=settings.JWT_EXPIRATION_DELTA)
            print(cache.get(user.token))

            ret['token'] = user.token
            ret['data'] = serializers.serialize('json', [user])

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}
            ret = {'code': 500, 'msg': str(e)}

        return JsonResponse(ret)