import datetime

from django.core.cache import cache
from django.http import JsonResponse
from App.models import *

# Create your views here.


# 粉丝数量/我的粉丝（查询接口）
def myfans(request):
    if request.method == "POST":
        loginuserid = cache.get('userid')
        # user = User.objects.get(id=1)

        if not loginuserid:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "未检测到用户已登录"}})
        user = User.objects.filter(id=loginuserid).first()
        # 根据个人id查询出粉丝id
        lfans = list(Concern.objects.filter(followers=user).values())

        # 查询粉丝id放入数组中用来到用户表查
        fanids = []
        for fanid in lfans:
            fanids.append(fanid["fans_id"])
        # 根据用户id列表表查询粉丝

        fanss = list(User.objects.filter(id__in = fanids).values("id","email","name","sex","sign","icon","date","tel"))
        fansss = []
        for i in fanss:
            # 如果这个粉丝被我关注过
            if Concern.objects.filter(fans_id= user.id,followers_id=i["id"]).first():
                i["isoncern"] = True
            else:
                i["isoncern"] = False
            fansss.append(i)

        data = {
        "code": 1,
        'msg': "success",
        "data": {
                'fansnum':len(fansss),
                'fans':fansss,
            }
        }
        return JsonResponse(data=data)
    elif request.method == "GET":
        return JsonResponse(data={"code":"0","msg":"fail","data":{"error":"别用GET请求啊"}})


# 我关注的数量/我关注的人（查询接口）
def myconcern(request):
    if request.method == "POST":
        loginuserid = cache.get('userid')
        # user = User.objects.get(id=1)

        if not loginuserid:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "未检测到用户已登录"}})
        user = User.objects.filter(id=loginuserid).first()
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


# 粉丝取消，（动作接口）也就是取消关注  需要传入用户id 不能是自己
def concernto(request):
    if request.method == "POST":
        loginuserid = cache.get('userid')
        # user = User.objects.get(id=1)

        if not loginuserid:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "未检测到用户已登录"}})
        user = User.objects.filter(id=loginuserid).first()
        userid = None
        try:
            userid = int(request.POST.get("userid"))
            if user.id == userid:
                return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "关注对象不能是自己"}})
        except:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "类型转换错误"}})
        # 判断传入的用户id是否有效
        if not User.objects.filter(id=userid).first():
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "该用户id不存在"}})

        # 查询是否关注过这个对象(如果存在这个粉丝
        fans = Concern.objects.filter(followers_id=userid,fans_id=user.id).first()
        # 如果已经关注过
        if fans:
            # 则取消关注
            fans.delete()
            JsonResponse(data={"code": "1", "msg": "success", "data": {"success": "已经取消对TA的关注"}})
        else:
            # 否则添加对象为关注对象
            Concern.objects.create(followers_id=userid,fans_id=user.id)
        data = {
            "code": 1,
            'msg': "success",
            "data": {
                "success": "关注TA成功"
            }
        }
        return JsonResponse(data=data)

    elif request.method == "GET":
        return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "别用GET请求啊"}})




# 喜欢我的人数/喜欢我的人,查询谁喜欢我 （查询接口）
def likeme(request):
    if request.method == "POST":
        loginuserid = cache.get('userid')
        # user = User.objects.get(id=1)

        if not loginuserid:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "未检测到用户已登录"}})
        user = User.objects.filter(id=loginuserid).first()
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


# 喜欢谁，点击to ,我要喜欢谁，或者我要取消喜欢谁（动作接口）
def liketo(request):
    if request.method == "POST":
        loginuserid = cache.get('userid')
        # user = User.objects.get(id=1)

        if not loginuserid:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "未检测到用户已登录"}})
        user = User.objects.filter(id=loginuserid).first()
        likeuserid = None
        try:
            likeuserid = int(request.POST.get("userid"))
            if user.id == likeuserid:
                return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "喜欢对象不能是自己"}})

        except:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "类型转换错误"}})
        # 判断传入的用户id是否有效
        if not User.objects.filter(id=likeuserid).first():
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "该用户id不存在"}})
        # 查询传入的id是否点击过喜欢
        userlikeme = LikePerson.objects.filter(user_id=likeuserid,user_like_id=user.id).first()
        if userlikeme:
            # 如果点击过喜欢
            userlikeme.delete()
            return JsonResponse(data={"code": "1", "msg": "success", "data": {"success": "已经取消喜欢"}})
        else:
            # 否则添加一条喜欢记录
            LikePerson.objects.create(user_id=likeuserid,user_like_id=user.id)

        data = {
            "code": 1,
            'msg': "success",
            "data": {
                "success": "成功给TA点击喜欢"
            }
        }
        return JsonResponse(data=data)

    elif request.method == "GET":
        return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "别用GET请求啊"}})



# 喜欢的壁纸数量/壁纸信息集合 （查询接口）
def mylikemural(request):
    if request.method == "POST":
        loginuserid = cache.get('userid')
        # user = User.objects.get(id=1)

        if not loginuserid:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "未检测到用户已登录"}})
        user = User.objects.filter(id=loginuserid).first()
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


# 点击喜欢的壁纸/取消喜欢的壁纸（动作接口）
def likemuralto(request):
    if request.method == "POST":
        loginuserid = cache.get('userid')
        # user = User.objects.get(id=1)

        if not loginuserid:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "未检测到用户已登录"}})
        user = User.objects.filter(id=loginuserid).first()
        muraid = None
        try:
            muraid = int(request.POST.get("muraid"))
        except:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "类型转换错误"}})

        # 查询是否给该壁纸点击过喜欢
        img = LikeMural.objects.filter(user_id=user.id,mural_id=muraid).first()
        if img:
            # 如果已经点击过
            img.delete()
        else:
            img = Mural.objects.filter(id=muraid).first()
            if not img:
                return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "壁纸id不存在"}})
            LikeMural.objects.create(user_id=user.id,mural_id=muraid)

        data = {
            "code": 1,
            'msg': "success",
            "data": {
                "success": "已给该壁纸点击喜欢"
            }
        }
        return JsonResponse(data=data)

    elif request.method == "GET":
        return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "别用GET请求啊"}})


# 查询收藏的壁纸/手账 （查询接口）
def collection(request):
    if request.method == "POST":
        loginuserid = cache.get('userid')
        # user = User.objects.get(id=1)

        if not loginuserid:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "未检测到用户已登录"}})
        user = User.objects.filter(id=loginuserid).first()
        # 查询用户收藏的手账
        handbook = list(UserImg.objects.filter(user_id=user.id,type=3,is_delete=0).values("path","type","info","upload_date"))
        # 查询用户收藏的壁纸
        mural = list(UserImg.objects.filter(user_id=user.id, type=4,is_delete=0).values("path","type","info","upload_date"))

        for i in handbook:
            img = Handbook.objects.filter(path=i["path"]).first()
            if not img:
                img = Mural.objects.filter(path=i["path"]).first()
            i["imgid"] = img.id

        for j in mural:
            img = Handbook.objects.filter(path=j["path"]).first()
            if not img:
                img = Mural.objects.filter(path=j["path"]).first()
            j["imgid"] = img.id


        data = {
            "code": 1,
            'msg': "success",
            "data": {
                "hanbook":handbook,
                "mural":mural,
            }
        }

        return JsonResponse(data=data)

    elif request.method == "GET":
        return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "别用GET请求啊"}})


# 用户收藏壁纸或手账（动作接口）
def collectionto(request):
    if request.method == "POST":
        loginuserid = cache.get('userid')
        # user = User.objects.get(id=1)

        if not loginuserid:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "未检测到用户已登录"}})
        user = User.objects.filter(id=loginuserid).first()
        imgid = None
        try:
            imgid = int(request.POST.get("imgid"))
        except:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "类型转换错误"}})
        img = Mural.objects.filter(id=imgid).first()
        if not img:
            img = Handbook.objects.filter(id=imgid).first()
            if not img:
                return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "图片id不存在"}})

        # 判断是否收藏过本手账或者图片
        userimg = UserImg.objects.filter(user_id=user.id)
        for usei in userimg:
            if img.path == usei.path:
                # 如果是已经被放入回收站的图片，则修改为未删除
                if usei.is_delete == 1:
                    usei.is_delete = 0
                    usei.save()
                    return JsonResponse(data={"code": "1", "msg": "success", "data": {"success": "已添加到收藏列表"}})
                usei.delete()
                return JsonResponse(data={"code": "1", "msg": "success", "data": {"success": "已从收藏列表中去除"}})

        # 获取图片是手账还是壁纸
        typ = Style.objects.get(id=img.type_id)
        # 如果是手账 ==1   混合  ==2    壁纸 ==3
        if typ.type == 1:
            UserImg.objects.create(path=img.path,type=3,is_delete=0,upload_date=datetime.datetime.now(),user=user)
        elif typ.type == 2:
            pass
        elif typ.type == 3:
            # 如果是壁纸
            UserImg.objects.create(path=img.path, type=4,is_delete=0,upload_date=datetime.datetime.now(), user=user)
        data = {
            "code": 1,
            'msg': "success",
            "data": {
                "success": "已添加到收藏列表"
            }
        }

        return JsonResponse(data=data)

    elif request.method == "GET":
        return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "别用GET请求啊"}})


# 显示回收站里的图片（查询接口）
def listrecover(request):
    if request.method == "POST":
        loginuserid = cache.get('userid')
        # user = User.objects.get(id=1)

        if not loginuserid:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "未检测到用户已登录"}})
        user = User.objects.filter(id=loginuserid).first()
        # 查询已经放入回收站的图片
        imgdel = list(UserImg.objects.filter(user_id=user.id,is_delete=1).values())


        data = {
            "code": 1,
            'msg': "success",
            "data": {
                "imgdel":imgdel,
            }
        }

        return JsonResponse(data=data)

    elif request.method == "GET":
        return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "别用GET请求啊"}})


# 恢复回收站里的图片，或者把图片移入回收站 (动作接口)
def recoverordelete(request):
    if request.method == "POST":
        loginuserid = cache.get('userid')
        # user = User.objects.get(id=1)

        if not loginuserid:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "未检测到用户已登录"}})
        user = User.objects.filter(id=loginuserid).first()
        imgid = None
        try:
            imgid = int(request.POST.get("imgid"))
        except:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "类型转换错误"}})
        img = Handbook.objects.filter(id=imgid).first()
        if not img:
            img = Mural.objects.filter(id=imgid).first()
            if not img:
                return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "图片id不存在"}})
        # 如果图片存在
        delimg = UserImg.objects.filter(user_id=user.id,path=img.path).first()
        if delimg:
            if delimg.is_delete == 1:
                delimg.is_delete = 0
                delimg.del_date = None
                delimg.save()
                return JsonResponse(data={"code": "1", "msg": "success", "data": {"success": "图片成功移出回收站"}})
            elif delimg.is_delete == 0:
                delimg.is_delete = 1
                delimg.del_date = datetime.datetime.now()
                delimg.save()
                return JsonResponse(data={"code": "1", "msg": "success", "data": {"success": "图片成功放入回收站"}})
        else:
            return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "该用户没有这个图片"}})
        data = {
            "code": 1,
            'msg': "success",
            "data": {

            }
        }

        return JsonResponse(data=data)

    elif request.method == "GET":
        return JsonResponse(data={"code": "0", "msg": "fail", "data": {"error": "别用GET请求啊"}})