#coding:utf-8
# 数据增删改查、统计分析到前端交互的完整接口
__author__ = "qing12315"
import base64, copy, logging, os, sys, time, xlrd, json, datetime, configparser
from django.http import JsonResponse
from django.apps import apps
from django.db.models.aggregates import Count,Sum
from django.db.models import Case, When, IntegerField, F
from django.forms import model_to_dict
from .models import jiuyeshuju
from util.codes import *
from util.auth import Auth
from util.common import Common
import util.message as mes
from django.db import connection
import random
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.db.models import Q
from util.baidubce_api import BaiDuBce
from .config_model import config






def jiuyeshuju_register(request):
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")


        error = jiuyeshuju.createbyreq(jiuyeshuju, jiuyeshuju, req_dict)
        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = "用户已存在,请勿重复注册!"
        return JsonResponse(msg)

def jiuyeshuju_login(request):
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")
        datas = jiuyeshuju.getbyparams(jiuyeshuju, jiuyeshuju, req_dict)
        if not datas:
            msg['code'] = password_error_code
            msg['msg'] = mes.password_error_code
            return JsonResponse(msg)

        try:
            __sfsh__= jiuyeshuju.__sfsh__
        except:
            __sfsh__=None

        if  __sfsh__=='是':
            if datas[0].get('sfsh')!='是':
                msg['code']=other_code
                msg['msg'] = "账号已锁定，请联系管理员审核!"
                return JsonResponse(msg)
                
        req_dict['id'] = datas[0].get('id')


        return Auth.authenticate(Auth, jiuyeshuju, req_dict)


def jiuyeshuju_logout(request):
    if request.method in ["POST", "GET"]:
        msg = {
            "msg": "登出成功",
            "code": 0
        }

        return JsonResponse(msg)


def jiuyeshuju_resetPass(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code}

        req_dict = request.session.get("req_dict")

        columns=  jiuyeshuju.getallcolumn( jiuyeshuju, jiuyeshuju)

        try:
            __loginUserColumn__= jiuyeshuju.__loginUserColumn__
        except:
            __loginUserColumn__=None
        username=req_dict.get(list(req_dict.keys())[0])
        if __loginUserColumn__:
            username_str=__loginUserColumn__
        else:
            username_str=username
        if 'mima' in columns:
            password_str='mima'
        else:
            password_str='password'

        init_pwd = '123456'
        recordsParam = {}
        recordsParam[username_str] = req_dict.get("username")
        records=jiuyeshuju.getbyparams(jiuyeshuju, jiuyeshuju, recordsParam)
        if len(records)<1:
            msg['code'] = 400
            msg['msg'] = '用户不存在'
            return JsonResponse(msg)

        eval('''jiuyeshuju.objects.filter({}='{}').update({}='{}')'''.format(username_str,username,password_str,init_pwd))
        
        return JsonResponse(msg)



def jiuyeshuju_session(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code,"msg": mes.normal_code, "data": {}}

        req_dict={"id":request.session.get('params').get("id")}
        msg['data']  = jiuyeshuju.getbyparams(jiuyeshuju, jiuyeshuju, req_dict)[0]

        return JsonResponse(msg)


def jiuyeshuju_default(request):

    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code,"msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        req_dict.update({"isdefault":"是"})
        data=jiuyeshuju.getbyparams(jiuyeshuju, jiuyeshuju, req_dict)
        if len(data)>0:
            msg['data']  = data[0]
        else:
            msg['data']  = {}
        return JsonResponse(msg)

def jiuyeshuju_page(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")

        global jiuyeshuju

        #获取全部列名
        columns=  jiuyeshuju.getallcolumn( jiuyeshuju, jiuyeshuju)

        if "vipread" in req_dict and "vipread" not in columns:
          del req_dict["vipread"]

        #当前登录用户所在表
        tablename = request.session.get("tablename")
            #authColumn=list(__authTables__.keys())[0]
            #authTable=__authTables__.get(authColumn)

            # if authTable==tablename:
                #params = request.session.get("params")
                #req_dict[authColumn]=params.get(authColumn)

        '''__authSeparate__此属性为真，params添加userid，后台只查询个人数据'''
        try:
            __authSeparate__=jiuyeshuju.__authSeparate__
        except:
            __authSeparate__=None

        if __authSeparate__=="是":
            tablename=request.session.get("tablename")
            if tablename!="users" and 'userid' in columns:
                try:
                    req_dict['userid']=request.session.get("params").get("id")
                except:
                    pass

        #当项目属性hasMessage为”是”，生成系统自动生成留言板的表messages，同时该表的表属性hasMessage也被设置为”是”,字段包括userid（用户id），username(用户名)，content（留言内容），reply（回复）
        #接口page需要区分权限，普通用户查看自己的留言和回复记录，管理员查看所有的留言和回复记录
        try:
            __hasMessage__=jiuyeshuju.__hasMessage__
        except:
            __hasMessage__=None
        if  __hasMessage__=="是":
            tablename=request.session.get("tablename")
            if tablename!="users":
                req_dict["userid"]=request.session.get("params").get("id")

        # 判断当前表的表属性isAdmin,为真则是管理员表
        # 当表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
        __isAdmin__ = None

        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__==tablename:

                try:
                    __isAdmin__ = m.__isAdmin__
                except:
                    __isAdmin__ = None
                break

        # 当前表也是有管理员权限的表
        if  __isAdmin__ == "是" and 'jiuyeshuju' != 'forum':
            if req_dict.get("userid") and 'jiuyeshuju' != 'chat':
                del req_dict["userid"]
        else:
            #非管理员权限的表,判断当前表字段名是否有userid
            if tablename!="users" and 'jiuyeshuju'[:7]!='discuss'and "userid" in jiuyeshuju.getallcolumn(jiuyeshuju,jiuyeshuju):
                req_dict["userid"] = request.session.get("params").get("id")

        #当列属性authTable有值(某个用户表)[该列的列名必须和该用户表的登陆字段名一致]，则对应的表有个隐藏属性authTable为”是”，那么该用户查看该表信息时，只能查看自己的
        try:
            __authTables__=jiuyeshuju.__authTables__
        except:
            __authTables__=None

        if __authTables__!=None and  __authTables__!={} and __isAdmin__ == "是":
            try:
                del req_dict['userid']
                # tablename=request.session.get("tablename")
                # if tablename=="users":
                    # del req_dict['userid']
                
            except:
                pass
            for authColumn,authTable in __authTables__.items():
                if authTable==tablename:
                    params = request.session.get("params")
                    req_dict[authColumn]=params.get(authColumn)
                    username=params.get(authColumn)
                    break
        q = Q()

        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  =jiuyeshuju.page(jiuyeshuju, jiuyeshuju, req_dict, request, q)

        return JsonResponse(msg)

def jiuyeshuju_autoSort(request):
    '''
    ．智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
主要信息列表（如商品列表，新闻列表）中使用，显示最近点击的或最新添加的5条记录就行
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")
        if "clicknum"  in jiuyeshuju.getallcolumn(jiuyeshuju,jiuyeshuju):
            req_dict['sort']='clicknum'
        elif "browseduration"  in jiuyeshuju.getallcolumn(jiuyeshuju,jiuyeshuju):
            req_dict['sort']='browseduration'
        else:
            req_dict['sort']='clicktime'
        req_dict['order']='desc'
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = jiuyeshuju.page(jiuyeshuju,jiuyeshuju, req_dict)

        return JsonResponse(msg)

#分类列表
def jiuyeshuju_lists(request):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":[]}
        msg['data'],_,_,_,_  = jiuyeshuju.page(jiuyeshuju, jiuyeshuju, {})
        return JsonResponse(msg)

def jiuyeshuju_list(request):
    '''
    前台分页
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        req_dict = request.session.get("req_dict")
        #获取全部列名
        columns=  jiuyeshuju.getallcolumn( jiuyeshuju, jiuyeshuju)
        if "vipread" in req_dict and "vipread" not in columns:
          del req_dict["vipread"]
        #表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
        try:
            __foreEndList__=jiuyeshuju.__foreEndList__
        except:
            __foreEndList__=None

        if __foreEndList__=="前要登":
            tablename=request.session.get("tablename")
            if tablename!="users" and 'userid' in columns:
                try:
                    req_dict['userid']=request.session.get("params").get("id")
                except:
                    pass
        #forrEndListAuth
        try:
            __foreEndListAuth__=jiuyeshuju.__foreEndListAuth__
        except:
            __foreEndListAuth__=None

        #authSeparate
        try:
            __authSeparate__=jiuyeshuju.__authSeparate__
        except:
            __authSeparate__=None

        if __foreEndListAuth__ =="是" and __authSeparate__=="是":
            tablename=request.session.get("tablename")
            if tablename!="users":
                req_dict['userid']=request.session.get("params",{"id":0}).get("id")

        tablename = request.session.get("tablename")
        if tablename == "users" and req_dict.get("userid") != None:#判断是否存在userid列名
            del req_dict["userid"]
        else:
            __isAdmin__ = None

            allModels = apps.get_app_config('main').get_models()
            for m in allModels:
                if m.__tablename__==tablename:

                    try:
                        __isAdmin__ = m.__isAdmin__
                    except:
                        __isAdmin__ = None
                    break

            if __isAdmin__ == "是":
                if req_dict.get("userid"):
                    # del req_dict["userid"]
                    pass
            else:
                #非管理员权限的表,判断当前表字段名是否有userid
                if "userid" in columns:
                    try:
                        pass
                    except:
                        pass
        #当列属性authTable有值(某个用户表)[该列的列名必须和该用户表的登陆字段名一致]，则对应的表有个隐藏属性authTable为”是”，那么该用户查看该表信息时，只能查看自己的
        try:
            __authTables__=jiuyeshuju.__authTables__
        except:
            __authTables__=None

        if __authTables__!=None and  __authTables__!={} and __foreEndListAuth__=="是":
            for authColumn,authTable in __authTables__.items():
                if authTable==tablename:
                    try:
                        del req_dict['userid']
                    except:
                        pass
                    params = request.session.get("params")
                    req_dict[authColumn]=params.get(authColumn)
                    username=params.get(authColumn)
                    break
        
        if jiuyeshuju.__tablename__[:7]=="discuss":
            try:
                del req_dict['userid']
            except:
                pass


        q = Q()
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = jiuyeshuju.page(jiuyeshuju, jiuyeshuju, req_dict, request, q)

        return JsonResponse(msg)

def jiuyeshuju_save(request):
    '''
    后台新增
    '''
    if request.method in ["POST", "GET"]:

        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        if 'clicktime' in req_dict.keys():
            del req_dict['clicktime']
        tablename=request.session.get("tablename")
        __isAdmin__ = None
        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__==tablename:

                try:
                    __isAdmin__ = m.__isAdmin__
                except:
                    __isAdmin__ = None
                break

        #获取全部列名
        columns=  jiuyeshuju.getallcolumn( jiuyeshuju, jiuyeshuju)
        if tablename!='users' and req_dict.get("userid")!=None and 'userid' in columns  and __isAdmin__!='是':
            params=request.session.get("params")
            req_dict['userid']=params.get('id')


        if 'addtime' in req_dict.keys():
            del req_dict['addtime']

        error= jiuyeshuju.createbyreq(jiuyeshuju,jiuyeshuju, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error

        return JsonResponse(msg)


def jiuyeshuju_add(request):
    '''
    前台新增就业数据记录的视图函数。处理 POST 或 GET 请求，根据请求数据创建新的就业数据记录。

    :param request: Django 的 HttpRequest 对象，包含请求的相关信息。
    :return: JsonResponse 对象，包含操作结果的状态码、消息和数据。
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        tablename=request.session.get("tablename")

        # 获取就业数据模型的全部列名
        columns=  jiuyeshuju.getallcolumn( jiuyeshuju, jiuyeshuju)
        try:
            __authSeparate__=jiuyeshuju.__authSeparate__
        except:
            __authSeparate__=None

        if __authSeparate__=="是":
            tablename=request.session.get("tablename")
            if tablename!="users" and 'userid' in columns:
                try:
                    req_dict['userid']=request.session.get("params").get("id")
                except:
                    pass

        try:
            # 尝试获取就业数据模型的 __foreEndListAuth__ 属性，用于判断前台列表的权限
            __foreEndListAuth__=jiuyeshuju.__foreEndListAuth__
        except:
            __foreEndListAuth__=None

        if __foreEndListAuth__ and __foreEndListAuth__!="否":
            tablename=request.session.get("tablename")
            if tablename!="users":
                req_dict['userid']=request.session.get("params").get("id")

        # 若请求数据字典中包含 addtime 字段，则删除该字段
        if 'addtime' in req_dict.keys():
            del req_dict['addtime']
        # 调用就业数据模型的 createbyreq 方法，根据请求数据创建新记录
        error= jiuyeshuju.createbyreq(jiuyeshuju,jiuyeshuju, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)

def jiuyeshuju_thumbsup(request,id_):
    '''
     点赞：表属性thumbsUp[是/否]，刷表新增thumbsupnum赞和crazilynum踩字段，
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        id_=int(id_)
        type_=int(req_dict.get("type",0))
        rets=jiuyeshuju.getbyid(jiuyeshuju,jiuyeshuju,id_)

        update_dict={
        "id":id_,
        }
        if type_==1:#赞
            update_dict["thumbsupnum"]=int(rets[0].get('thumbsupnum'))+1
        elif type_==2:#踩
            update_dict["crazilynum"]=int(rets[0].get('crazilynum'))+1
        error = jiuyeshuju.updatebyparams(jiuyeshuju,jiuyeshuju, update_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def jiuyeshuju_info(request,id_):
    '''
    根据传入的 ID 获取就业数据的详细信息，并在需要时更新浏览点击次数。

    :param request: Django 的 HttpRequest 对象，包含请求的相关信息。
    :param id_: 要查询的就业数据记录的 ID。
    :return: JsonResponse 对象，包含操作结果的状态码、消息和详细数据。
    '''
    if request.method in ["POST", "GET"]:
        # 初始化返回消息，默认状态码和消息表示操作正常
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        # 根据 ID 获取就业数据记录
        data = jiuyeshuju.getbyid(jiuyeshuju,jiuyeshuju, int(id_))
        if len(data)>0:
            msg['data']=data[0]
            if msg['data'].__contains__("reversetime"):
                if isinstance(msg['data']['reversetime'], datetime.datetime):
                    msg['data']['reversetime'] = msg['data']['reversetime'].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    if msg['data']['reversetime'] != None:
                        reversetime = datetime.datetime.strptime(msg['data']['reversetime'], '%Y-%m-%d %H:%M:%S')
                        msg['data']['reversetime'] = reversetime.strftime("%Y-%m-%d %H:%M:%S")

        # 尝试获取就业数据模型的 __browseClick__ 属性，用于判断是否需要统计浏览点击次数
        try:
            __browseClick__= jiuyeshuju.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__=="是"  and  "clicknum"  in jiuyeshuju.getallcolumn(jiuyeshuju,jiuyeshuju):
            try:
                clicknum=int(data[0].get("clicknum",0))+1
            except:
                clicknum=0+1
            click_dict={"id":int(id_),"clicknum":clicknum}
            ret=jiuyeshuju.updatebyparams(jiuyeshuju,jiuyeshuju,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return JsonResponse(msg)

def jiuyeshuju_detail(request,id_):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data =jiuyeshuju.getbyid(jiuyeshuju,jiuyeshuju, int(id_))
        if len(data)>0:
            msg['data']=data[0]
            if msg['data'].__contains__("reversetime"):
                if isinstance(msg['data']['reversetime'], datetime.datetime):
                    msg['data']['reversetime'] = msg['data']['reversetime'].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    if msg['data']['reversetime'] != None:
                        reversetime = datetime.datetime.strptime(msg['data']['reversetime'], '%Y-%m-%d %H:%M:%S')
                        msg['data']['reversetime'] = reversetime.strftime("%Y-%m-%d %H:%M:%S")

        #浏览点击次数
        try:
            __browseClick__= jiuyeshuju.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__=="是"   and  "clicknum"  in jiuyeshuju.getallcolumn(jiuyeshuju,jiuyeshuju):
            try:
                clicknum=int(data[0].get("clicknum",0))+1
            except:
                clicknum=0+1
            click_dict={"id":int(id_),"clicknum":clicknum}

            ret=jiuyeshuju.updatebyparams(jiuyeshuju,jiuyeshuju,click_dict)
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return JsonResponse(msg)

def jiuyeshuju_update(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        if 'clicktime' in req_dict.keys() and req_dict['clicktime']=="None":
            del req_dict['clicktime']
        if req_dict.get("mima") and "mima" not in jiuyeshuju.getallcolumn(jiuyeshuju,jiuyeshuju) :
            del req_dict["mima"]
        if req_dict.get("password") and "password" not in jiuyeshuju.getallcolumn(jiuyeshuju,jiuyeshuju) :
            del req_dict["password"]
        try:
            del req_dict["clicknum"]
        except:
            pass


        error = jiuyeshuju.updatebyparams(jiuyeshuju, jiuyeshuju, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error

        return JsonResponse(msg)


def jiuyeshuju_delete(request):
    '''
    批量删除就业数据记录的视图函数，支持 POST 和 GET 请求方式。
    根据请求数据中的 ID 列表，批量删除对应的就业数据记录。

    :param request: Django 的 HttpRequest 对象，包含请求的相关信息。
    :return: JsonResponse 对象，包含操作结果的状态码、消息和数据。
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")

        # 调用 jiuyeshuju 模型的 deletes 方法，传入模型自身、模型自身以及请求数据中的 ID 列表，执行批量删除操作
        error=jiuyeshuju.deletes(jiuyeshuju,
            jiuyeshuju,
             req_dict.get("ids")
        )
        # 若删除过程中出现错误
        if error != None:
            # 修改状态码为操作错误码
            msg['code'] = crud_error_code
            # 修改消息为错误信息
            msg['msg'] = error
        return JsonResponse(msg)

def jiuyeshuju_vote(request,id_):
    '''
    浏览点击次数（表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1）
统计商品或新闻的点击次数；提供新闻的投票功能
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code}


        data= jiuyeshuju.getbyid(jiuyeshuju, jiuyeshuju, int(id_))
        for i in data:
            votenum=i.get('votenum')
            if votenum!=None:
                params={"id":int(id_),"votenum":votenum+1}
                error=jiuyeshuju.updatebyparams(jiuyeshuju,jiuyeshuju,params)
                if error!=None:
                    msg['code'] = crud_error_code
                    msg['msg'] = error
        return JsonResponse(msg)

def jiuyeshuju_importExcel(request):
    """
    处理 Excel 文件导入请求，将 Excel 中的就业数据导入到系统中。

    :param request: Django 的 HttpRequest 对象，包含请求的相关信息。
    :return: JsonResponse 对象，包含操作结果的状态码和消息。
    """
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}

        # 从请求中获取上传的 Excel 文件，若未提供则为空字符串
        excel_file = request.FILES.get("file", "")
        # 通过文件名分割获取文件扩展名
        file_type = excel_file.name.split('.')[1]
        
        if file_type in ['xlsx', 'xls']:
            data = xlrd.open_workbook(filename=None, file_contents=excel_file.read())
            table = data.sheets()[0]
            rows = table.nrows

            # 检查文件类型是否为 Excel 格式
            try:
                for row in range(1, rows):
                    row_values = table.row_values(row)
                    req_dict = {}
                    if '.0' in str(row_values[0]):
                        req_dict['xueli'] = str(row_values[0]).split('.')[0]
                    elif str(row_values[0]) != '':
                        req_dict['xueli'] = row_values[0]
                    else:
                        req_dict['xueli'] = None
                    if '.0' in str(row_values[1]):
                        req_dict['zhuanye'] = str(row_values[1]).split('.')[0]
                    elif str(row_values[1]) != '':
                        req_dict['zhuanye'] = row_values[1]
                    else:
                        req_dict['zhuanye'] = None
                    if '.0' in str(row_values[2]):
                        req_dict['jiuyedanwei'] = str(row_values[2]).split('.')[0]
                    elif str(row_values[2]) != '':
                        req_dict['jiuyedanwei'] = row_values[2]
                    else:
                        req_dict['jiuyedanwei'] = None
                    if '.0' in str(row_values[3]):
                        req_dict['danweixingzhi'] = str(row_values[3]).split('.')[0]
                    elif str(row_values[3]) != '':
                        req_dict['danweixingzhi'] = row_values[3]
                    else:
                        req_dict['danweixingzhi'] = None
                    if '.0' in str(row_values[4]):
                        req_dict['zhiweileibie'] = str(row_values[4]).split('.')[0]
                    elif str(row_values[4]) != '':
                        req_dict['zhiweileibie'] = row_values[4]
                    else:
                        req_dict['zhiweileibie'] = None
                    if '.0' in str(row_values[5]):
                        req_dict['danweixingye'] = str(row_values[5]).split('.')[0]
                    elif str(row_values[5]) != '':
                        req_dict['danweixingye'] = row_values[5]
                    else:
                        req_dict['danweixingye'] = None
                    if '.0' in str(row_values[6]):
                        req_dict['danweisuozaidi'] = str(row_values[6]).split('.')[0]
                    elif str(row_values[6]) != '':
                        req_dict['danweisuozaidi'] = row_values[6]
                    else:
                        req_dict['danweisuozaidi'] = None
                    if '.0' in str(row_values[7]):
                        req_dict['gangweixinchou'] = str(row_values[7]).split('.')[0]
                    elif str(row_values[7]) != '':
                        req_dict['gangweixinchou'] = row_values[7]
                    else:
                        req_dict['gangweixinchou'] = None
                    if '.0' in str(row_values[8]):
                        req_dict['value'] = str(row_values[8]).split('.')[0]
                    elif str(row_values[8]) != '':
                        req_dict['value'] = row_values[8]
                    else:
                        req_dict['value'] = None
                    if '.0' in str(row_values[9]):
                        req_dict['name'] = str(row_values[9]).split('.')[0]
                    elif str(row_values[9]) != '':
                        req_dict['name'] = row_values[9]
                    else:
                        req_dict['name'] = None
                    jiuyeshuju.createbyreq(jiuyeshuju, jiuyeshuju, req_dict)
                    
            except:
                # 若导入过程中出现异常，不做处理
                pass
                
        else:
            # 若文件类型不是 Excel 格式，更新返回消息
            msg = {
                "msg": "文件类型错误",
                "code": 500
            }
                
        return JsonResponse(msg)

def jiuyeshuju_autoSort2(request):
    return JsonResponse({"code": 0, "msg": '',  "data":{}})

# （按值统计）时间统计类型
def jiuyeshuju_value(request, xColumnName, yColumnName, timeStatType):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        
        where = ' where 1 = 1 '
        sql = ''
        if timeStatType == '日':
            sql = "SELECT DATE_FORMAT({0}, '%Y-%m-%d') {0}, sum({1}) total FROM jiuyeshuju {2} GROUP BY DATE_FORMAT({0}, '%Y-%m-%d')".format(xColumnName, yColumnName, where, '%Y-%m-%d')

        if timeStatType == '月':
            sql = "SELECT DATE_FORMAT({0}, '%Y-%m') {0}, sum({1}) total FROM jiuyeshuju {2} GROUP BY DATE_FORMAT({0}, '%Y-%m')".format(xColumnName, yColumnName, where, '%Y-%m')

        if timeStatType == '年':
            sql = "SELECT DATE_FORMAT({0}, '%Y') {0}, sum({1}) total FROM jiuyeshuju {2} GROUP BY DATE_FORMAT({0}, '%Y')".format(xColumnName, yColumnName, where, '%Y')

        L = []
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()] 
        for online_dict in data_dict:
            for key in online_dict:
                if 'datetime.datetime' in str(type(online_dict[key])):
                    online_dict[key] = online_dict[key].strftime(
                        "%Y-%m-%d %H:%M:%S")
                else:
                    pass
            L.append(online_dict)
        msg['data'] = L
        return JsonResponse(msg)

# 按值统计
def jiuyeshuju_o_value(request, xColumnName, yColumnName):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        
        where = ' where 1 = 1 '
        
        sql = "SELECT {0}, sum({1}) AS total FROM jiuyeshuju {2} GROUP BY {0} LIMIT 10".format(xColumnName, yColumnName, where)
        L = []
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()] 
        for online_dict in data_dict:
            for key in online_dict:
                if 'datetime.datetime' in str(type(online_dict[key])):
                    online_dict[key] = online_dict[key].strftime(
                        "%Y-%m-%d %H:%M:%S")
                else:
                    pass
            L.append(online_dict)
        msg['data'] = L
        return JsonResponse(msg)

# （按值统计）时间统计类型(多)
def jiuyeshuju_valueMul(request, xColumnName, timeStatType):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": []}

        req_dict = request.session.get("req_dict")

        where = ' where 1 = 1 '
        
        for item in req_dict['yColumnNameMul'].split(','):
            sql = ''
            if timeStatType == '日':
                sql = "SELECT DATE_FORMAT({0}, '%Y-%m-%d') {0}, sum({1}) total FROM jiuyeshuju {2} GROUP BY DATE_FORMAT({0}, '%Y-%m-%d') LIMIT 10".format(xColumnName, item, where, '%Y-%m-%d')

            if timeStatType == '月':
                sql = "SELECT DATE_FORMAT({0}, '%Y-%m') {0}, sum({1}) total FROM jiuyeshuju {2} GROUP BY DATE_FORMAT({0}, '%Y-%m') LIMIT 10".format(xColumnName, item, where, '%Y-%m')

            if timeStatType == '年':
                sql = "SELECT DATE_FORMAT({0}, '%Y') {0}, sum({1}) total FROM jiuyeshuju {2} GROUP BY DATE_FORMAT({0}, '%Y') LIMIT 10".format(xColumnName, item, where, '%Y')

            L = []
            cursor = connection.cursor()
            cursor.execute(sql)
            desc = cursor.description
            data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()] 
            for online_dict in data_dict:
                for key in online_dict:
                    if 'datetime.datetime' in str(type(online_dict[key])):
                        online_dict[key] = online_dict[key].strftime(
                            "%Y-%m-%d %H:%M:%S")
                    else:
                        pass
                L.append(online_dict)
            msg['data'].append(L)
        return JsonResponse(msg)

# （按值统计(多)）
def jiuyeshuju_o_valueMul(request, xColumnName):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": []}

        req_dict = request.session.get("req_dict")
        
        where = ' where 1 = 1 '

        for item in req_dict['yColumnNameMul'].split(','):
            sql = "SELECT {0}, sum({1}) AS total FROM jiuyeshuju {2} GROUP BY {0} LIMIT 10".format(xColumnName, item, where)
            L = []
            cursor = connection.cursor()
            cursor.execute(sql)
            desc = cursor.description
            data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()] 
            for online_dict in data_dict:
                for key in online_dict:
                    if 'datetime.datetime' in str(type(online_dict[key])):
                        online_dict[key] = online_dict[key].strftime(
                            "%Y-%m-%d %H:%M:%S")
                    else:
                        pass
                L.append(online_dict)
            msg['data'].append(L)

        return JsonResponse(msg)



def jiuyeshuju_count(request):
    '''
    总数接口
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        req_dict = request.session.get("req_dict")
        where = ' where 1 = 1 '
        for key in req_dict:
            if req_dict[key] != None:
                where = where + " and key like '{0}'".format(req_dict[key])
        
        sql = "SELECT count(*) AS count FROM jiuyeshuju {0}".format(where)
        count = 0
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()] 
        for online_dict in data_dict:
            count = online_dict['count']
        msg['data'] = count

        return JsonResponse(msg)

def jiuyeshuju_group(request, columnName):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        
        where = ' where 1 = 1 '

        sql = "SELECT COUNT(*) AS total, " + columnName + " FROM jiuyeshuju " + where + " GROUP BY " + columnName

        L = []
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()] 
        for online_dict in data_dict:
            for key in online_dict:
                if 'datetime.datetime' in str(type(online_dict[key])):
                    online_dict[key] = online_dict[key].strftime("%Y-%m-%d")
                else:
                    pass
            L.append(online_dict)
        msg['data'] = L
        return JsonResponse(msg)



