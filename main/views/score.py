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
            data = models.Score.objects.filter(student__uid=uid).order_by('pk')
            data = serializers.serialize('json', data, use_natural_foreign_keys=True)
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
    # 管理员查询任务的体测数据
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            task_id = request.GET.get('task_id', None)
            page_num = request.GET.get('page_num', 1)
            key = request.GET.get('search_key', None)
            value = request.GET.get('search_value', '')
            if task_id is None:
                return JsonResponse({'code': 400, 'msg': '任务id不能为空'})
            data = models.Score.objects.filter(
                task_id=task_id,
            ).order_by('pk')
            if key:
                key += '__icontains'
                data = data.filter(**{key: value})
            data, ret['page_count'] = tools.myPaginator(data, 20, page_num)
            data = serializers.serialize('json', data)
            ret['data'] = data

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}
            print(str(e))

        return JsonResponse(ret)
    

class ScoreStatics(APIView):
    # 单个任务的成绩统计
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
            grade = request.GET.get('grade', 'low')
            if models.ScoreStandard.objects.filter(grade=grade).count() == 0:
                models.ScoreStandard.objects.create(grade=grade)
            
            data = models.ScoreStandard.objects.filter(grade=grade).values(key)
            # ret['data'] = serializers.serialize('json', data)
            ret['data'] = json.dumps(list(data)[0])

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}
            ret = {'code': 500, 'msg': 'Timeout', 'error': str(e)}

        return JsonResponse(ret)
    
    # 修改一个项目的评分标准
    def put(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            data = json.loads(request.body).get('data', {})
            key = data.get('key', '')
            grade = data.get('grade', 'low')
            value = data.get('value', '[]')
            
            try:
                value = json.dumps(value)
            except Exception as e:
                return JsonResponse({'code': 400, 'msg': '格式错误'})
            # validate data

            models.ScoreStandard.objects.filter(grade=grade).update_or_create(
                defaults={key: value},
            )

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)
    

class ClassInfomation(APIView):
    # 获取全校的班级信息
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            data = models.ClassInfomation.objects.all()
            ret['data'] = serializers.serialize('json', data)

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}
            ret = {'code': 500, 'msg': 'Timeout', 'error': str(e)}

        return JsonResponse(ret)