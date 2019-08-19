from django.urls import path, include

from Relative.views import *

urlpatterns = [
    # 我关注的数量/我关注的人（查询接口）---------测试通过
    path('myconcern/',myconcern,name='myconcern'),
    # 关注/取消关注（动作接口）       --------测试通过
    path('concernto/',concernto,name='concernto'),

    # 喜欢人数/喜欢我的人（查询接口）  ---------测试通过
    path('likeme/',likeme,name='likeme'),
    # 点击喜欢的人/取消喜欢的人（动作接口）  --------测试通过
    path('liketo/',liketo,name="liketo"),


    # 喜欢的壁纸数量/壁纸信息集合（查询接口） -------测试通过
    path('mylikemural/',mylikemural,name='mylikemural'),
    # 点击喜欢的壁纸/取消喜欢的壁纸（动作接口） ------测试通过
    path('likemuralto/',likemuralto,name='likemuralto'),

    # 粉丝数量/我的粉丝（查询接口） -------测试通过
    path('myfans/',myfans,name='myfans'),


    # 查询收藏的壁纸/手账 （查询接口）
    path('collection/',collection,name= 'collection'),
    # 收藏壁纸/手账 （动作接口）    --------测试通过
    path('collectionto/',collectionto,name= 'collectionto'),

    # 显示回收站里的图片（查询接口）      --------测试通过
    path('listrecover/',listrecover,name= 'listrecover'),
    # 恢复回收站里的图片，或者把图片移入回收站 (动作接口)  ------测试通过
    path('recoverordelete/',recoverordelete,name= 'recoverordelete'),
]