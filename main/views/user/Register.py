from django.http import JsonResponse
from rest_framework.views import APIView

from main import models
from main import tools

import json


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