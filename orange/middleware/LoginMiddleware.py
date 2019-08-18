<<<<<<< HEAD
=======
from django.contrib.auth.hashers import check_password
>>>>>>> pqw
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect,reverse
from  django.utils.deprecation import MiddlewareMixin

from App.models import User


class LoginMiddleware(MiddlewareMixin):
    def process_request(self,request):
<<<<<<< HEAD
        path_list = ['/orange/user/info/','/orange/relative/fans/','/orange/relative/concern/','/orange/relative/fanscancle/','/orange/relative/like/','/orange/relative/collection/','/orange/relative/likemural/']  #如果在这个列表就需要验证是否登陆
        #同url 排除get请求的需要自己加if判断
        if request.path in path_list:
            userid = cache.get('userid')
            if not userid:
                return JsonResponse({'msg': '请先登陆', 'code': 0})
=======
        path_list = ['/orange/user/login/','/orange/user/info/','/orange/relative/fans/','/orange/relative/concern/','/orange/relative/fanscancle/','/orange/relative/like/','/orange/relative/collection/','/orange/relative/likemural/', '/orange/home/upload/', '/orange/home/handpeople/']  #如果在这个列表就需要验证是否登陆
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
>>>>>>> pqw
            else:
                request.user = User.objects.get(pk = userid)


