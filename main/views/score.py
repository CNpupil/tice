from rest_framework.views import APIView
from django.core import serializers
from django.http import JsonResponse

from main import models
from main import tools, tice_tools

import json

class ScoreOnStudent(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            uid = request.GET.get('uid', None)
            if uid is None:
                return JsonResponse({'code': 400, 'msg': '学号不能为空'})
            data = models.Score.objects.filter(student_uid=uid).order_by('pk')
            data = serializers.serialize('json', data)
            ret['data'] = data

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)
    

class ScoreOnTask(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            task_id = request.GET.get('task_id', None)
            page_num = request.GET.get('page_num', 1)
            if task_id is None:
                return JsonResponse({'code': 400, 'msg': '任务id不能为空'})
            data = models.Score.objects.filter(task_id=task_id).order_by('pk')
            data, ret['page_count'] = tools.myPaginator(data, 20, page_num)
            data = serializers.serialize('json', data)
            ret['data'] = data

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)


class ScoreOnSearch(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            task_id = request.GET.get('task_id', None)
            page_num = request.GET.get('page_num', 1)
            key = request.GET.get('search_key', 'uid')
            value = request.GET.get('value', '')
            if task_id is None:
                return JsonResponse({'code': 400, 'msg': '任务id不能为空'})
            data = models.Score.objects.filter(
                task_id=task_id,
                **{key: value}
            ).order_by('pk')
            data, ret['page_count'] = tools.myPaginator(data, 20, page_num)
            data = serializers.serialize('json', data)
            ret['data'] = data

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)
    

class ScoreStatics(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            task_id = request.GET.get('task_id', None)
            if task_id is None:
                return JsonResponse({'code': 400, 'msg': '任务id不能为空'})
            scores = models.Score.objects.filter(task_id=task_id)

            # 计算新生年级
            task = models.Task.objects.filter(pk=task_id).first()
            freshman_grade = task.year
            if task.half == 1:
                freshman_grade = task.year - 1

            # 拿出全部end_score去统计
            end_score_list = [t['end_score'] for t in scores.values('end_score')]
            tag_statics =  tice_tools.calc_tags_count(end_score_list)
            ret['data'] = tag_statics

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)
    


class calculate_score(APIView):
    # 给定一个数据计算相应的分数
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            key = request.GET.get('key', '')
            value = request.GET.get('value', '')
            grad_level = request.GET.get('grad_level', 'low')

            calc = tice_tools.CalcScore(grad_level)
            ret['data'] = calc.calc_item_score(key, value)

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)
    

class ScoreStandard(APIView):
    # 获取一个项目的评分标准
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            key = request.GET.get('key', '')
            if models.ScoreStandard.objects.all().count() == 0:
                models.ScoreStandard.objects.create()
            
            data = models.ScoreStandard.all()
            ret['data'] = serializers.serialize('json', data)

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)
    
    # 修改一个项目的评分标准
    def put(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            data = json.loads(request.body).get('data', {})
            key = data.get('key', '')
            value = data.get('value', '[]')
            
            try:
                json.loads(value)
            except Exception as e:
                return JsonResponse({'code': 400, 'msg': '格式错误'})
            # validate data

            models.ScoreStandard.objects.update_or_create(
                defaults={key: value},
                pk=1
            )

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)