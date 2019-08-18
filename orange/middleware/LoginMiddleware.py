
from django.contrib.auth.hashers import check_password

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect,reverse
from  django.utils.deprecation import MiddlewareMixin

from App.models import User


class LoginMiddleware(MiddlewareMixin):
    def process_request(self,request):


        path_list = ['/orange/user/login/','/orange/user/info/', '/orange/home/upload/',
                     '/orange/home/handpeople/','/orange/relative/myconcern/','/orange/relative/concernto/',
                     '/orange/relative/likeme/','/orange/relative/liketo/','/orange/relative/mylikemural/',
                     '/orange/relative/likemuralto/','/orange/relative/myfans/','/orange/relative/collectionto/',
                     '/orange/relative/listrecover/','/orange/relative/recoverordelete/',]  #如果在这个列表就需要验证是否登陆
        #同url 排除get请求的需要自己加if判断
        if request.path in path_list:
            userid = cache.get('userid')

            print(userid)
            if not userid:
                if request.path == '/orange/user/login/':
                    email = request.POST.get('email')
                    password = request.POST.get('password')

                    print(email)
                    user = User.objects.get(email=email)
                    if check_password(password, user.password):
                        request.user = user
                        cache.set("userid", user.id)

                        return JsonResponse({'msg': '登陆成功', 'code': 1})
                else:
                    return JsonResponse({'msg': '请先登陆', 'code': 0})

            else:
                request.user = User.objects.get(pk = userid)


