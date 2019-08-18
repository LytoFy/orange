from django.http import JsonResponse
from django.shortcuts import redirect,reverse
from  django.utils.deprecation import MiddlewareMixin

from App.models import User


class LoginMiddleware(MiddlewareMixin):
    def process_request(self,request):
        path_list = ['/modifyinfo/']  #如果在这个列表就需要验证是否登陆
        #同url 排除get请求的需要自己加if判断

        if request.path in path_list:
            userid = request.cache.get('userid')
            if not userid:

                return JsonResponse({'msg': '请先登陆', 'code': 0})
            else:
                request.user = User.objects.get(pk = userid)

