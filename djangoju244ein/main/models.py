#coding:utf-8
# 定义毕业生模型
__author__ = "qing12315"
from django.db import models

from .model import BaseModel

from datetime import datetime



class biyesheng(BaseModel):
    """
    定义毕业生信息的数据库模型类。

    Attributes:
        __doc__ (str): 类的文档字符串，描述该类代表毕业生信息。
        __tablename__ (str): 表名，对应数据库中的表名。
        __loginUser__ (str): 登录用户所使用的字段名，这里为 'xuehao'（学号）。
        __authTables__ (dict): 认证相关的表信息，初始为空字典。
        __authPeople__ (str): 是否为用户表的标识，'是' 表示是用户表。
        __loginUserColumn__ (str): 用户表中代表用户名的字段，这里为 'xuehao'。
        __sfsh__ (str): 是否审核的标识，'否' 表示不需要审核。
        __authSeparate__ (str): 后台列表权限标识，'否' 表示无特殊权限。
        __thumbsUp__ (str): 是否启用点赞踩功能，'否' 表示不启用。
        __intelRecom__ (str): 是否启用智能推荐功能，'否' 表示不启用。
        __browseClick__ (str): 是否启用浏览点击和投票功能，'否' 表示不启用。
        __foreEndListAuth__ (str): 前台列表权限标识，'否' 表示无特殊权限。
        __foreEndList__ (str): 前台列表页面是否存在的标识，'否' 表示不存在。
        __isAdmin__ (str): 是否为管理员表的标识，'否' 表示不是管理员表。
        addtime (models.DateTimeField): 记录创建时间的字段。
        xuehao (models.CharField): 学号字段，唯一且不能为空。
        mima (models.CharField): 密码字段，不能为空。
        xingming (models.CharField): 姓名字段，不能为空。
        xingbie (models.CharField): 性别字段，可为空。
        zhuanye (models.CharField): 专业字段，可为空。
        touxiang (models.TextField): 头像字段，可为空。
    """
    __doc__ = u'''biyesheng'''
    __tablename__ = 'biyesheng'

    __loginUser__='xuehao'


    __authTables__={}
    __authPeople__='是'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __loginUserColumn__='xuehao'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    xuehao=models.CharField ( max_length=255,null=False,unique=True, verbose_name='学号' )
    mima=models.CharField ( max_length=255,null=False, unique=False, verbose_name='密码' )
    xingming=models.CharField ( max_length=255,null=False, unique=False, verbose_name='姓名' )
    xingbie=models.CharField ( max_length=255, null=True, unique=False, verbose_name='性别' )
    zhuanye=models.CharField ( max_length=255, null=True, unique=False, verbose_name='专业' )
    touxiang=models.TextField   (  null=True, unique=False, verbose_name='头像' )
    '''
    xuehao=VARCHAR
    mima=VARCHAR
    xingming=VARCHAR
    xingbie=VARCHAR
    zhuanye=VARCHAR
    touxiang=Text
    '''
    class Meta:
        db_table = 'biyesheng'
        verbose_name = verbose_name_plural = '毕业生'
class jiuyeshuju(BaseModel):
    __doc__ = u'''jiuyeshuju'''
    __tablename__ = 'jiuyeshuju'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    xueli=models.CharField ( max_length=255, null=True, unique=False, verbose_name='学历' )
    zhuanye=models.CharField ( max_length=255, null=True, unique=False, verbose_name='专业' )
    jiuyedanwei=models.CharField ( max_length=255, null=True, unique=False, verbose_name='就业单位' )
    danweixingzhi=models.CharField ( max_length=255, null=True, unique=False, verbose_name='单位性质' )
    zhiweileibie=models.CharField ( max_length=255, null=True, unique=False, verbose_name='职位类别' )
    danweixingye=models.CharField ( max_length=255, null=True, unique=False, verbose_name='单位行业' )
    danweisuozaidi=models.CharField ( max_length=255, null=True, unique=False, verbose_name='单位所在地' )
    gangweixinchou=models.IntegerField  (  null=True, unique=False, verbose_name='岗位薪酬' )
    value=models.IntegerField  (  null=True, unique=False, verbose_name='数量' )
    name=models.CharField ( max_length=255, null=True, unique=False, verbose_name='地区' )
    '''
    xueli=VARCHAR
    zhuanye=VARCHAR
    jiuyedanwei=VARCHAR
    danweixingzhi=VARCHAR
    zhiweileibie=VARCHAR
    danweixingye=VARCHAR
    danweisuozaidi=VARCHAR
    gangweixinchou=Integer
    value=Integer
    name=VARCHAR
    '''
    class Meta:
        db_table = 'jiuyeshuju'
        verbose_name = verbose_name_plural = '就业数据'
class gonggaoxinxi(BaseModel):
    __doc__ = u'''gonggaoxinxi'''
    __tablename__ = 'gonggaoxinxi'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    gonggaobiaoti=models.CharField ( max_length=255,null=False, unique=False, verbose_name='公告标题' )
    leixing=models.CharField ( max_length=255,null=False, unique=False, verbose_name='类型' )
    tupian=models.TextField   (  null=True, unique=False, verbose_name='图片' )
    neirong=models.TextField   (  null=True, unique=False, verbose_name='内容' )
    faburiqi=models.DateField   (  null=True, unique=False, verbose_name='发布日期' )
    lianjie=models.CharField ( max_length=255, null=True, unique=False, verbose_name='链接' )
    '''
    gonggaobiaoti=VARCHAR
    leixing=VARCHAR
    tupian=Text
    neirong=Text
    faburiqi=Date
    lianjie=VARCHAR
    '''
    class Meta:
        db_table = 'gonggaoxinxi'
        verbose_name = verbose_name_plural = '公告信息'
class systemintro(BaseModel):
    __doc__ = u'''systemintro'''
    __tablename__ = 'systemintro'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    title=models.CharField ( max_length=255,null=False, unique=False, verbose_name='标题' )
    subtitle=models.CharField ( max_length=255, null=True, unique=False, verbose_name='副标题' )
    content=models.TextField   ( null=False, unique=False, verbose_name='内容' )
    picture1=models.TextField   (  null=True, unique=False, verbose_name='图片1' )
    picture2=models.TextField   (  null=True, unique=False, verbose_name='图片2' )
    picture3=models.TextField   (  null=True, unique=False, verbose_name='图片3' )
    '''
    title=VARCHAR
    subtitle=VARCHAR
    content=Text
    picture1=Text
    picture2=Text
    picture3=Text
    '''
    class Meta:
        db_table = 'systemintro'
        verbose_name = verbose_name_plural = '系统简介'
