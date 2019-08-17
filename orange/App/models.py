from __future__ import unicode_literals

from django.db import models


class Buy(models.Model):
    '''
        用户购买手账模型
    '''
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True, verbose_name='用户')
    handbook = models.ForeignKey('Handbook', models.DO_NOTHING, blank=True, null=True, verbose_name='手账')
    date = models.DateTimeField(auto_now_add=True,verbose_name='购买时间')

    class Meta:
        db_table = 'buy'

    @property
    def to_dict(self):
        return {'id': self.id, 'user': self.user, 'handbook': self.handbook, 'date': self.date}


class Concern(models.Model):
    '''
        关注和粉丝表
    '''
    followers = models.ForeignKey('User',related_name='followers_fk', blank=True, null=True, verbose_name='关注', on_delete=models.DO_NOTHING)
    fans = models.ForeignKey('User', related_name='fans_fk', blank=True, null=True, verbose_name='粉丝', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now=True, verbose_name="关注时间")

    class Meta:
        db_table = 'concern'

    @property
    def to_dict(self):
        return {'id': self.id, 'followers': self.followers, 'fans': self.fans, 'date': self.date}


class Handbook(models.Model):
    '''
        手账表
    '''
    path = models.CharField(max_length=255, blank=True, null=True, verbose_name='手账的地址')
    type = models.ForeignKey('Style', models.DO_NOTHING, blank=True, null=True, verbose_name='手账分类')
    price = models.FloatField(blank=True, null=True, verbose_name='手账价格')
    date = models.DateTimeField(auto_now=True, verbose_name='手账上传时间')

    class Meta:
        db_table = 'handbook'

    @property
    def to_dict(self):
        return {'id': self.id, 'path': self.path, 'type': self.type,'price': self.price,'date': self.date}


class LikeMural(models.Model):
    '''
        用户喜欢壁纸表
    '''
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True, verbose_name='用户')
    mural = models.ForeignKey('Mural', models.DO_NOTHING, blank=True, null=True, verbose_name='壁纸表')
    date = models.DateTimeField(auto_now=True, verbose_name="用户收藏的时间")

    class Meta:
        db_table = 'like_mural'

    @property
    def to_dict(self):
        return {'id': self.id, 'user': self.user, 'mural': self.mural,'date': self.date}


class LikePerson(models.Model):
    '''
        用户对用户的喜欢
    '''
    user_like = models.ForeignKey('User', models.DO_NOTHING, related_name='user_like_fk',blank=True, null=True, verbose_name="喜欢的用户")
    user = models.ForeignKey('User', models.DO_NOTHING, related_name='user_fk',blank=True, null=True, verbose_name="被喜欢的用户")

    class Meta:
        db_table = 'like_person'

    @property
    def to_dict(self):
        return {'id': self.id, 'user_like': self.user_like, 'muuserral': self.user}


class Mural(models.Model):
    '''
        壁纸表
    '''
    path = models.CharField(max_length=255, blank=True, null=True, verbose_name='图片位置')
    type = models.ForeignKey('Style', models.DO_NOTHING, blank=True, null=True, verbose_name='壁纸分类')
    date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mural'

    @property
    def to_dict(self):
        return {'id': self.id, 'path': self.path, 'type': self.type, 'date': self.date}


class Style(models.Model):
    '''
        类型表, 对手账和壁纸的分类。
            type:1 ------ 手账
            type:2 ------ 壁纸
            type:3 ------ 手账和壁纸
    '''
    name = models.CharField(max_length=25, blank=True, null=True, verbose_name='分类名称')
    type = models.IntegerField(blank=True, null=True, verbose_name='手账和壁纸的分开类型')

    class Meta:
        db_table = 'style'

    @property
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'type': self.type}



class User(models.Model):
    '''
        用户表
    '''
    email = models.CharField(max_length=30, verbose_name='邮箱')
    name = models.CharField(max_length=20,default='更换昵称', blank=True, null=True, verbose_name='昵称')
    sex = models.IntegerField(blank=True, null=True, verbose_name='性别')
    sign = models.CharField(max_length=255, blank=True, null=True, verbose_name='个人发布的签名')
    password = models.CharField(max_length=255, blank=True, null=True)
    icon = models.CharField(max_length=255, blank=True, null=True, verbose_name='个人图像')
    date = models.DateField(auto_now_add=True, verbose_name="用户创建时间")
    tel = models.CharField(max_length=12, blank=True, null=True, verbose_name="用户电话号码")

    class Meta:
        db_table = 'user'

    @property
    def to_dict(self):
        return {'id': self.id, 'email': self.email, 'name': self.name, 'sex': self.sex, 'sign': self.sign,'icon': self.icon,'date': self.date,'tel': self.tel}


class UserImg(models.Model):
    '''
        用户上传的图片
            type: 1 用户发布的手账
            type: 2 用户发布的壁纸
            type：3 用户收藏的手账
            type：4 用户收藏的壁纸
    '''
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, verbose_name='用户信息')
    path = models.CharField(max_length=255, blank=True, null=True, verbose_name="上传的地址")
    type = models.IntegerField(blank=True, null=True, verbose_name="图片的分类")
    info = models.CharField(max_length=255, blank=True, null=True, verbose_name="图片的描述")
    upload_date = models.DateTimeField(blank=True, null=True, verbose_name="图片上传时间")
    del_date = models.DateField(blank=True, null=True, verbose_name="图片删除时间")
    is_delete = models.IntegerField(blank=True, null=True, verbose_name="是否删除，判断图片是否可见")

    class Meta:
        db_table = 'user_img'

    @property
    def to_dict(self):
        return {'id': self.id, 'user': self.user, 'path': self.path, 'type': self.type, 'info': self.info, 'upload_date': self.upload_date}

