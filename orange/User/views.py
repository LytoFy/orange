import random

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render

import smtplib        # 使用这个模块可以模拟邮箱的登录
from email.mime.text import MIMEText    # 生成右键使用

# Create your views here.
from django.views import View
from App.models import *

import logging

from App.views import Upload

inf_logger = logging.getLogger('inf')

def verifyEmail(ema,ver):
    print('-----------------------------')
    # 授权码
    auCode = "ftnhwiwoeiwjbecb"
    fromEmail = "970524784@qq.com"  # 这个授权码，就是发送邮箱的授权码
    toEmail = ema
    smtpSever = "smtp.qq.com"  # 邮箱服务器地址
    port = 25  # 邮件服务的端口

    smtp = smtplib.SMTP(smtpSever, port)
    print("=====",smtp)
    # 登录
    smtp.login(fromEmail, auCode)
    print(smtp.login(fromEmail, auCode))

    # 生成邮件
    msg = MIMEText("欢迎注册小橘子，这里有精美的壁纸福利，快来领取，验证码是：%s，请在五分钟内完成验证。真的会过期的啊，还不快点！"%ver)
    msg["Subject"] = "orange小橘子验证码"  # 邮件的标题
    msg['From'] = fromEmail
    msg['To'] = toEmail

    print('-------========',123456)
    # 发送邮件  msg.as_string() 像邮件一样发送
    smtp.sendmail(fromEmail, toEmail, msg.as_string())
    print('==-=--=-=-==-=',smtp)
    # 关闭
    return 1


class Register(View):

    def get(self,request):
        email = request.GET.get('email')
        if not email:
            return JsonResponse({'code':'0','msg':'邮箱为空'})
        verify = random.randint(1000,9999)
        n=0
        n=verifyEmail(email,verify)
        cache.set('verify',str(verify),300)

        return JsonResponse({'code':n,'msg':'邮箱已发送，等待时间过程可能邮箱错误'})


    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        verify = request.POST.get('verify')
        sub_verify = cache.get('verify')
        if not (email and password and verify):
            return JsonResponse({'code':'0','msg':'有为空选项'})
        if verify == sub_verify:
            user = User.objects.filter(email=email).first()
            if user:
                data = {
                    'code':'0',
                    'msg':'用户已存在'
                }
                return JsonResponse(data)
            else:
                user = User()
                user.email=email
                user.password = make_password(password)
                user.save()
                inf_logger.info("%s注册成功" % email)
                data = {
                    'code': '1',
                    'msg': '用户注册成功'
                }
            return JsonResponse(data)
        data = {
            'code': '0',
            'msg': '验证码错误'
        }
        return JsonResponse(data)


class Login(View):
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not (email and password):
            return JsonResponse({'code':'0','msg':'有为空选项'})
        user = User.objects.filter(email=email).first()
        if user:
            if check_password(password, user.password):
                cache.set('userid',user.id,60*60*24)
                request.session['userid']=user.id
                request.session.set_expiry(60 * 60 * 24)
                inf_logger.info("%s登陆成功" % email)
                date = {
                    'code': 1,
                    'msg': '用户登陆成功'
                }
                return  JsonResponse(date)
            else:
                data = {
                    'code': 0,
                    'msg': '密码不正确'
                }
                return JsonResponse(data)
        else:
            data = {
                'code': 0,
                'msg': '用户名不正确'
            }
            return JsonResponse(data)

class Loginout(View):
    def get(self,request):
        inf_logger.info("%s注销成功" % request.session.get('userid'))
        cache.delete('userid')
        request.session.delete("userid")
        data = {
            'code': '1',
            'msg': '用户注销成功'
        }
        return JsonResponse(data)


class ModifyInfo(View):
    def post(self,request):
        data = {
            'code': '0',
            'msg': '信息修改失败',
        }
        name = request.POST.get('name')
        sign = request.POST.get('sign')
        sex = request.POST.get('sex')
        icon = request.FILES.get('icon')
        if not (name or  sign or sex or icon):
            return JsonResponse({'code':'0','msg':'不能为空'})
        userid = cache.get('userid')
        if userid:
            user = User.objects.filter(id=userid).first()
            if name:
                user.name=name
                user.save()
                data['code']="1"
                data['msg']="用户名修改成功"
                data['name']=name
                inf_logger.info("%s修改成功" % name)
            if sign:
                user.sign=sign
                user.save()
                data['code'] = "1"
                data['msg'] = "个性签名修改成功"
                data['sign'] = sign
            if sex:
                user.sex=sex
                user.save()
                data['code'] = "1"
                data['msg'] = "性别修改成功"
                if sex=='1':
                    data['sex'] = '男'
                elif sex =='0':
                    data['sex'] = '女'
                else:
                    data['code'] = "0"
                    data['msg'] = "性别修改失败"
                    data['sex'] = '输入错误'
            if icon:
                up = Upload()
                icon=up.file(icon)
                user.icon=icon
                #头像存储
                user.save()
                data['code'] = "1"
                data['msg'] = "头像修改成功"
                data['icon'] = icon
            inf_logger.info("%s修改成功" % str(userid))
            return JsonResponse(data)
        return JsonResponse(data)

class Info(View):
    def get(self,requsert):

        userid = cache.get('userid')
        user = User.objects.filter(id=userid)
        fans = len(Concern.objects.filter(followers_id=userid))
        followers = len(Concern.objects.filter(fans_id=userid))
        like_num = len(LikePerson.objects.filter(user_id=userid))
        user = list(user.values('id','name','sex','sign','icon'))

        data={
            'code': '1',
            'msg': '信息获取',
            'user':user,
            'followers':followers,
            'fans':fans,
            'like_num':like_num,

        }
        inf_logger.info("%获取成功" % str(userid))

        return JsonResponse(data)



class Find(View):

    def get(self,request):
        findtext = request.GET.get('findtext')
        if findtext:
            find = []
            for i in findtext:
                find1 = User.objects.filter(name__contains=i)
                find2 = Handbook.objects.filter(name__contains=i)
                find3 = Style.objects.filter(name__contains=i)
                findend = list(find1.values_list('name'))+list(find2.values_list('name'))+list(find3.values_list('name'))
                findend = list(set(findend))
                for value in findend:
                    find.append(value[0])
            data = {
                'code': '1',
                'msg': '信息获取',
                'find':find,
            }
            return JsonResponse(data)
        else:
            data = {
                'code': '0',
                'msg': '失败',
            }
            return JsonResponse(data)
    def post(self,request):
        findtext = request.POST.get('findtext')
        find1 = User.objects.filter(name=findtext)
        find2 = Handbook.objects.filter(name=findtext)
        find3 = Style.objects.filter(name=findtext).first()

        info = []
        handbook = []
        muralimg = []
        if find1:
            for i in find1:
                try:
                    like_num = len(LikePerson.objects.filter(user_id=i.id))
                    iscenter = Concern.objects.filter(fans_id=cache.get('userid'),followers_id=i.id).exists()
                    user_img = list(UserImg.objects.filter(user_id=i.id).values('path','type'))
                    info.append({'id':i.id,'name':i.name,'icon':i.icon,'like_num':like_num,'iscenter':iscenter,'user_img':user_img})
                except:
                    return JsonResponse({'code':0,"msg":"不正确使用"})
        if find2:
            for i in find2:
                handimg = list(Handbook.objects.filter(name=i.name).values())
                handbook.append({'path':handimg})

        if find3:
            muraltype = find3.type
            if muraltype >= 2:
                muralimg = list(Mural.objects.filter(type_id=find3.id).values())
            if muraltype <= 2:
                muralimg = list(Handbook.objects.filter(type_id=find3.id).values())


        data = {
            'code': '1',
            'msg': '查找信息',
            'info':info,
            'handbook':handbook,
            'mural':muralimg
        }
        return JsonResponse(data)


