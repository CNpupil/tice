from rest_framework.views import APIView
from django.core import serializers
from django.http import JsonResponse

from main import models
from main import tools, tice_tools
from main.tice_tools import consruct_item

import json





class ScoreOnStudent(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            uid = request.GET.get('uid', None)
            if uid is None:
                return JsonResponse({'code': 400, 'msg': '学号不能为空'})
            data = models.Score.objects.filter(student__uid=uid).order_by('pk')

            tables = []
            for score in data:
                table = []
                tables.append(consruct_item('bmi', '{}, {}'.format(score.height, score.weight), score.bmi_score))
                table.append(consruct_item('肺活量', score.pulmonary, score.pulmonary_score))
                table.append(consruct_item('坐位体前屈', score.jump, score.jump_score))
                table.append(consruct_item('跳远', score.jump, score.jump_score))
                table.append(consruct_item('50m', score.run50, score.run50_score))
                table.append(consruct_item('800m/1000m', score.run800 if score.student.sex == 2 else score.run1000, score.runlong_score))
                table.append(consruct_item('仰卧起坐/引体向上', score.adbominal_curl if score.student.sex == 2 else score.pull_up, score.curlorup_score))
                table.append(consruct_item('左眼视力', score.left_eye, None))
                table.append(consruct_item('右眼视力', score.right_eye, None))
                table.append(consruct_item('最终分数', score.right_eye, None))
                table.append(consruct_item('等级', score.right_eye, None))
                tables.append({score.task_id: table})
            
            ret['tables'] = json.dumps(tables)
            data = serializers.serialize('json', data, use_natural_foreign_keys=True)
            ret['data'] = data

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}
            print(str(e))

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
            task_id = request.GET.get('task_id', -1)
            search_key = request.GET.get('search_key', None)
            search_value = request.GET.get('search_value', None)

            items = {'grade', 'college', 'major', 'class_name'}
            filter_criteria = {}
            for item in items:
                if request.GET.get(item, None):
                    filter_criteria['student__' + item] = request.GET.get(item)

            data = models.Score.objects.filter(
                task_id = task_id,
                ** filter_criteria
            ).order_by('student_id')
            if search_key:
                search_key += '__icontains'
                data = data.filter(**{search_key:search_value})

            data, ret['page_count'] = tools.myPaginator(data, 20, request.GET.get('page_num', 1))

            ret['data'] = serializers.serialize('json', data, use_natural_foreign_keys=True)

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}

        return JsonResponse(ret)
    

# class ScoreStatics(APIView):
#     # 单个任务的成绩统计
#     def get(self, request, *args, **kwargs):
#         ret = {'code': 200, 'msg': 'ok'}
#         try:
#             task_id = request.GET.get('task_id', None)
#             if task_id is None:
#                 return JsonResponse({'code': 400, 'msg': '任务id不能为空'})
#             scores = models.Score.objects.filter(task_id=task_id)

#             # 计算新生年级
#             task = models.Task.objects.filter(pk=task_id).first()
#             freshman_grade = task.year
#             if task.half == 1:
#                 freshman_grade = task.year - 1

#             # 拿出全部end_score去统计
#             end_score_list = [t['end_score'] for t in scores.values('end_score')]
#             tag_statics =  tice_tools.calc_tags_count(end_score_list)
#             ret['data'] = tag_statics

#         except Exception as e:
#             ret = {'code': 500, 'msg': 'Timeout'}

#         return JsonResponse(ret)
    

class ScoreStatics(APIView):
    # 单个任务的成绩统计
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': 'ok'}
        try:
            data = json.loads(request.body).get('data', {})
            task_id = data.get('task_id', None)
            items = data.get('items', [])
            statics_names = data.get('statics_names', [])
            if task_id is None:
                return JsonResponse({'code': 400, 'msg': '任务id不能为空'})
            data = {}
            for item in items:
                data[item] = {}
                for statics_name in statics_names:
                    data[item][statics_name] = tice_tools.calc_item_statics(task_id, item, statics_name)
            
            ret['data'] = json.dumps(data)

        except Exception as e:
            ret = {'code': 500, 'msg': 'Timeout'}
            ret = {'code': 500, 'msg': 'Timeout', 'error': str(e)}

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