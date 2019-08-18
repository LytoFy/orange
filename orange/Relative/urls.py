from django.urls import path, include

from Relative.views import *

urlpatterns = [
    # 我关注的数量/我关注的人
    path('concern',concern,name='concern'),
    # 喜欢人数/喜欢我的人
    path('like',like,name='like'),
    # 粉丝数量/我的粉丝
    path('fans',fans,name='fans'),
    # 关注/取消关注
    path('fanscancle',fanscancle,name='fanscancle'),
    # 喜欢的壁纸数量/壁纸信息集合
    path('likemural',likemural,name='mural'),
    # 收藏壁纸/手账
    path('collection',collection,name='collection'),
    # 发布壁纸/手账
]