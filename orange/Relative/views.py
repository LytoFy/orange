import datetime

from django.http import JsonResponse
from App.models import *

# Create your views here.


# 粉丝数量/我的粉丝
def fans(request):
    if request.method == "POST":
        # user = request.user

        user = User.objects.get(id=2)
        if not user:
            return JsonResponse(data={"code":"0","msg":"fail","data":{"error":"未检测到用户已登录"}})
        # 根据个人id查询出粉丝id
        lfans = list(Concern.objects.filter(followers=user).values())
        # 查询粉丝id放入数组中用来到用户表查
        fanids = []
        for fanid in lfans:
            fanids.append(fanid["id"])
        # 根据用户id列表表查询粉丝

        fanss = list(User.objects.filter(id__in = fanids).values("id","email","name","sex","sign","icon","date","tel"))

        data = {
        "code": 1,
        'msg': "success",
        "data": {
                'fansnum':len(fanss),
                'fans':fanss,
            }
        }
        return JsonResponse(data=data)
    elif request.method == "GET":
        return JsonResponse(data={"code":"0","msg":"fail","data":{"error":"别用GET请求啊"}})


# 我关注的数量/我关注的人
def concern(request):
    if request.method == "POST":
        # user = request.user

        user = User.objects.get(id=3)

        if not user:
            return JsonResponse(data={"code":"0","msg":"fail","data":{"error":"未检测到用户已登录"}})
        # 查询 我做为为粉丝的用户id  我关注的用户id
        lconcern = list(Concern.objects.filter(fans=user).values("followers"))
        # 关注对象的id  列表集
        concrenids = []
        for concid in lconcern:
            concrenids.append(concid["followers"])
        concerns = list(
            User.objects.filter(id__in=concrenids).values("id", "email", "name", "sex", "sign", "icon", "date", "tel"))
        data = {
            "code": 1,
            'msg': "success",
            "data": {
                "concernnum":len(concerns),
                "concern": concerns,
            }
        }
        return JsonResponse(data=data)

    elif request.method == "GET":
        return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "别用GET请求啊"}})


# 粉丝取消，也就是取消关注  需要传入用户id 不能是自己
def fanscancle(request):
    if request.method == "POST":
        # user = request.user
        user = User.objects.get(id=1)  # 有 2 ， 4 两个粉丝
        if not user:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "未检测到用户已登录"}})
        userid = None
        try:
            userid = int(request.POST.get("userid"))
            if user.id == userid:
                return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "关注对象不能是自己"}})
        except:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "类型转换错误"}})
        print(userid)
        # 查询是否关注过这个对象(如果存在这个粉丝
        fans = LikePerson.objects.filter(user_id=user.id,user_like_id=userid).first()
        # 如果已经关注过
        if fans:
            # 则取消关注
            fans.delete()
        else:
            # 否则添加对象为关注对象
            LikePerson.objects.create(user_id=user.id,user_like_id=userid)
        data = {
            "code": 1,
            'msg': "success",
            "data": {

            }
        }
        return JsonResponse(data=data)

    elif request.method == "GET":
        return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "别用GET请求啊"}})




# 喜欢我的人数/喜欢我的人
def like(request):
    if request.method == "POST":
        # user = request.user

        user = User.objects.get(id=1)

        if not user:
            return JsonResponse(data={"code":"0","msg":"fail","data":{"error":"未检测到用户已登录"}})
        # 查找  给我点喜欢的人的id
        llike = list(LikePerson.objects.filter(user=user).values("user_like_id"))
        likeid = []
        for lik in llike:
            likeid.append(lik["user_like_id"])
        likes = list(
            User.objects.filter(id__in=likeid).values("id", "email", "name", "sex", "sign", "icon", "date", "tel"))

        data = {
            "code": 1,
            'msg': "success",
            "data": {
                "likenum":len(likes),
                "likes":likes,
            }
        }
        return JsonResponse(data=data)

    elif request.method == "GET":
        return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "别用GET请求啊"}})

# 喜欢的壁纸数量/壁纸信息集合
def likemural(request):
    if request.method == "POST":
        # user = request.user

        user = User.objects.get(id=1)

        if not user:
            return JsonResponse(data={"code":"0","msg":"fail","data":{"error":"未检测到用户已登录"}})
        # 查找  喜欢的壁纸的 的id字典
        lmural = list(LikeMural.objects.filter(user=user).order_by("date").values("mural"))
        # 获取壁纸id的集合
        muraids = []
        for mur in lmural:
            muraids.append(mur["mural"])
        # 根据id集合查询壁纸集合
        likemurals = list(Mural.objects.filter(id__in=muraids).values())
        # 最终返回结果，在末尾追加一个type:{}
        likemural = []
        for likem in likemurals:
            # 追加类型type{id:**,name:**,typeid:**}
            likem["type"] = Style.objects.get(id=likem["type_id"]).to_dict
            likemural.append(likem)
        print(likemural)

        data = {
            "code": 1,
            'msg': "success",
            "data": {
                "likemuralnum":len(likemural),
                "likemural":likemural,
            }
        }
        return JsonResponse(data=data)

    elif request.method == "GET":
        return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "别用GET请求啊"}})


# 用户收藏壁纸或手账
def collection(request):
    if request.method == "POST":
        # user = request.user

        user = User.objects.get(id=1)

        if not user:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "未检测到用户已登录"}})
        typeid = None
        try:
            typeid = int(request.POST.get("typeid"))
        except:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "类型转换错误"}})
        img = Mural.objects.get(type=typeid)
        # 获取图片是手账还是壁纸
        typ = Style.objects.get(id=typeid)
        print(typ.type)
        # 如果是手账 ==1   混合  ==2    壁纸 ==3
        if typ.type == 1:
            UserImg.objects.create(path=img.path,type=3,upload_date=datetime.datetime.now(),user=user)
        elif typ.type == 2:
            pass
        elif typ.type == 3:
            # 如果是壁纸
            UserImg.objects.create(path=img.path, type=4, upload_date=datetime.datetime.now(), user=user)
        data = {
            "code": 1,
            'msg': "success",
            "data": {

            }
        }
        return JsonResponse(data=data)

    elif request.method == "GET":
        return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "别用GET请求啊"}})


