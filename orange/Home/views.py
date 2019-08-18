from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from App.models import *


class MarkIndex(View):
    '''
        首页：集市
    '''

    def get(self, request):
        '''
            首页界面, 可能是手账或者壁纸

        '''

        data = {
            "code": "1",
            "msg": "success",
            "data": [

            ]
        }
        curr_id = request.GET.get("type", 1)
        print(curr_id)
        if 1 == int(curr_id):
            # 手账主要类型
            types = list(Style.objects.filter(type=1).values())
            # 去手账表获取一张图片返回给前端
            for type_obj in types:
                img = Handbook.objects.filter(type_id=int(type_obj.get("id"))).first().path
                type_obj["img"] = img

            data["data"] = types
            return JsonResponse(data)
        elif 2 == int(curr_id):
            # 壁纸
            types = list(Style.objects.filter(type=2).values())
            # 去手账表获取一张图片返回给前端
            for type_obj in types:
                img = Mural.objects.filter(type_id=int(type_obj.get("id"))).first().path
                type_obj["img"] = img

            data["data"] = types
            return JsonResponse(data)
        else:
            data["code"] = 0
            data["msg"] = "请求参数错误"
            return JsonResponse(data)


class NBPeople(View):
    '''
        达人中心
    '''

    def get(self, request):
        data = {
            "code": 1,
            "msg": "success",
            "data": [

            ]
        }
        curr_id = request.GET.get("type")
        curr_user = "pqw"
        if 1 == int(curr_id):
            # 手账达人
            users = list(User.objects.filter().order_by('date').values('id', "name", 'icon'))

            for people in users:
                # 找每个人的喜欢的人
                print(people)
                num = LikePerson.objects.filter(user_id=people.get("id")).count()
                is_fans = False
                if LikePerson.objects.filter().exists():
                    is_fans = True
                people["num"] = num
                people["is_fans"] = is_fans

                handimg = list(
                    UserImg.objects.filter(user_id=people.get("id"), type=1, is_delete=0).values('id', 'path'))[:3]
                people['hand_img'] = handimg
            data["data"] = users
            return JsonResponse(data)
        elif 2 == int(curr_id):
            # 壁纸达人
            users = list(User.objects.filter().order_by('date').values('id', "name", 'icon'))

            for people in users:
                # 找每个人的喜欢的人
                print(people)
                num = LikePerson.objects.filter(user_id=people.get("id")).count()
                is_fans = False
                if LikePerson.objects.filter().exists():
                    is_fans = True
                people["num"] = num
                people["is_fans"] = is_fans

                picimg = list(
                    UserImg.objects.filter(user_id=people.get("id"), type=2, is_delete=0).values('id', 'path'))[:3]
                people['pic_img'] = picimg
            data["data"] = users
            return JsonResponse(data)
        else:
            data["code"] = 0,
            data["msg"] = "非法的参数请求"
            return JsonResponse(data)


class TempHand(View):
    '''
        上传手账的时候，可以选择的模板
    '''

    def get(self, request, *args):
        data = {
            "code": 1,
            "msg": "success",
            "data": [

            ]
        }
        if not args[0]:
            try:
                books = list(Handbook.objects.filter().values())
                data["data"] = books
                return JsonResponse(data)
            except:
                data["code"] = 0
                data["msg"] = "服务器内部错误"

                return JsonResponse(data)
        else:
            try:
                books = list(Handbook.objects.filter(id=int(args[0])).values())
                data["data"] = books
                return JsonResponse(data)
            except:
                data["code"] = 0
                data["msg"] = "服务器内部错误"
                return JsonResponse(data)


class MarkHand(View):
    '''
        处理集市相关的请求。
    '''

    def get(self, request):
        data = {
            "code": 1,
            "msg": "success",
            "data": [

            ]
        }

        # 获取相关的分类
        if int(request.GET.get("mark")) == 1 and not request.GET.get("typeid"):
            # 获取手账的分类
            lists = list(Style.objects.filter(type=1).values())
            data["data"] = lists
            return JsonResponse(data)
        elif int(request.GET.get("mark"))  == 2 and not request.GET.get("typeid"):
            # 获取手账的分类
            lists = list(Style.objects.filter(type=1).values())
            data["data"] = lists
            return JsonResponse(data)



        # 分类类型id
        hand_type = int(request.GET.get("typeid", 0))
        if 1 == int(request.GET.get("mark")):
            # 手账集市

            books = list(Handbook.objects.filter(type_id=int(hand_type)).values())

            name = Style.objects.filter(pk=hand_type).first().name
            for book in books:
                book["name"] = name
            data["data"] = books
            return JsonResponse(data)
        elif 2 == int(request.GET.get("mark")):
            # 壁纸集市
            books = list(Mural.objects.filter(type_id=int(hand_type)).values())
            name = Style.objects.filter(pk=hand_type).first().name
            print(name)
            for book in books:
                book["name"] = name
            data["data"] = books
            return JsonResponse(data)
        else:
            data["code"] = 0
            data['msg'] = "输入参数错误"
            return JsonResponse(data)

