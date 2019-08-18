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
inf_logger = logging.getLogger('inf')

def verifyEmail(ema,ver):
    # 授权码
    auCode = "juhlknddtmxpbbab"
    fromEmail = "970524784@qq.com"  # 这个授权码，就是发送邮箱的授权码
    toEmail = ema
    smtpSever = "smtp.qq.com"  # 邮箱服务器地址
    port = 25  # 邮件服务的端口

    smtp = smtplib.SMTP(smtpSever, port)
    # 登录
    smtp.login(fromEmail, auCode)

    # 生成邮件
    msg = MIMEText("验证码是：%s"%ver)
    msg["Subject"] = "orange验证"  # 邮件的标题
    msg['From'] = fromEmail
    msg['To'] = toEmail

    # 发送邮件  msg.as_string() 像邮件一样发送
    smtp.sendmail(fromEmail, toEmail, msg.as_string())

    # 关闭
    smtp.close()


class Register(View):

    def get(self,request):
        email = request.GET.get('email')
        if not email:
            return JsonResponse({'code':'0','msg':'邮箱为空'})
        verify = random.randint(1000,9999)
        verifyEmail(email,verify)
        cache.set('verify',str(verify),300)
        return JsonResponse({'code':'0','msg':'邮箱已发送，等待时间过程可能邮箱错误'})


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
                inf_logger.info(f"%s注册成功" % email)
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
        password = check_password(password,make_password(password))
        if email and password:
            return JsonResponse({'code':'0','msg':'有为空选项'})
        user = User.objects.filter(email=email,password=password).first()
        if user:
            cache.set('userid',user.id)
            inf_logger.info(f"%s登陆成功" % email)
            date = {
                'code': 1,
                'msg': '用户登陆成功'
            }
            return  JsonResponse(date)
        else:
            data = {
                'code': 0,
                'msg': '用户名或密码不正确'
            }
            return JsonResponse(data)

class Loginout(View):
    def get(self,request):
        inf_logger.info(f"%s注销成功" % request.session.get('userid'))
        cache.delete('userid')
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
        if name or sign or sex or icon:
            return JsonResponse({'code':'0','msg':'不能为空'})
        userid = cache.get('userid')
        user = User.objects.filter(id=userid).first()
        if name:
            user.name=name
            user.save()
            data['code']="1"
            data['msg']="用户名修改成功"
            data['name']=name
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
            # user.icon=icon
            #头像存储
            user.save()
            data['code'] = "1"
            data['msg'] = "头像修改成功"
            data['icon'] = icon

        return JsonResponse(data)

class Info(View):
    def get(self,requsert):
        userid = cache.get('userid')
        user = User.objects.filter(id=userid)
        user = list(user.values('id','name','sex','sign','icon'))
        data={
            'code': '1',
            'msg': '信息获取',
            'user':user
        }
        return JsonResponse(data)