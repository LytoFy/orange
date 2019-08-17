from django.urls import path, include
from .views import *

urlpatterns = [
    path("login/", Login.as_view(), name='login'),
    path("register/", Register.as_view(), name='register'),
    path("loginout/", Loginout.as_view(), name='loginout'),
    path("modifyinfo/", ModifyInfo.as_view(), name='modifyinfo'),
    path("info/", Info.as_view(), name='info'),
]