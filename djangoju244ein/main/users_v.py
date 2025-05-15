# coding:utf-8
# 处理个人信息视图逻辑
__author__ = "qing12315"

from django.http import JsonResponse

from .users_model import users
from util.codes import *
from util.auth import Auth
import util.message as mes
from dj2.settings import host,port,user,passwd,dbName,hasHadoop

def users_login(request):
    """
    处理用户登录请求。根据请求数据查询用户信息，并进行身份验证。

    :param request: Django 的 HttpRequest 对象，包含请求的相关信息。
    :return: JsonResponse 对象，包含登录操作的状态码和消息，或身份验证结果。
    """
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        # 从会话中获取请求数据字典
        req_dict = request.session.get("req_dict")
        if req_dict.get('role')!=None:
            del req_dict['role']

        # 根据请求数据查询用户信息
        datas = users.getbyparams(users, users, req_dict)
        if not datas:
            msg['code'] = password_error_code
            msg['msg'] = mes.password_error_code
            return JsonResponse(msg)

        # 将查询到的用户 ID 添加到请求数据字典中
        req_dict['id'] = datas[0].get('id')
        # 调用 Auth 类的 authenticate 方法进行身份验证
        return Auth.authenticate(Auth, users, req_dict)


def users_register(request):
    if request.method in ["POST", "GET"]:
        msg = {'code': normal_code, "msg": mes.normal_code}
        req_dict = request.session.get("req_dict")

        error = users.createbyreq(users, users, req_dict)
        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def users_session(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code,"msg":mes.normal_code, "data": {}}

        req_dict = {"id": request.session.get('params').get("id")}
        msg['data'] = users.getbyparams(users, users, req_dict)[0]

        return JsonResponse(msg)


def users_logout(request):
    if request.method in ["POST", "GET"]:
        msg = {
            "msg": "退出成功",
            "code": 0
        }

        return JsonResponse(msg)


def users_page(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code,
               "data": {"currPage": 1, "totalPage": 1, "total": 1, "pageSize": 10, "list": []}}
        req_dict = request.session.get("req_dict")
        tablename = request.session.get("tablename")
        try:
            __hasMessage__ = users.__hasMessage__
        except:
            __hasMessage__ = None
        if __hasMessage__ and __hasMessage__ != "否":

            if tablename != "users":
                req_dict["userid"] = request.session.get("params").get("id")
        if tablename == "users":
            msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
            msg['data']['pageSize'] = users.page(users, users, req_dict)
        else:
            msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
            msg['data']['pageSize'] = [],1,0,0,10

        return JsonResponse(msg)


def users_info(request, id_):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}

        data = users.getbyid(users, users, int(id_))
        if len(data) > 0:
            msg['data'] = data[0]
        # 浏览点击次数
        try:
            __browseClick__ = users.__browseClick__
        except:
            __browseClick__ = None

        if __browseClick__ and "clicknum" in users.getallcolumn(users, users):
            click_dict = {"id": int(id_), "clicknum": str(int(data[0].get("clicknum", 0)) + 1)}
            ret = users.updatebyparams(users, users, click_dict)
            if ret != None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return JsonResponse(msg)


def users_save(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        req_dict['role'] = '管理员'
        error = users.createbyreq(users, users, req_dict)
        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def users_update(request):
    '''
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")
        if req_dict.get("mima") and req_dict.get("password"):
            if "mima" not in users.getallcolumn(users,users):
                del req_dict["mima"]
            if "password" not in users.getallcolumn(users,users):
                del req_dict["password"]
        try:
            del req_dict["clicknum"]
        except:
            pass
        error = users.updatebyparams(users, users, req_dict)
        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)


def users_delete(request):
    '''
    处理用户删除请求，支持 POST 和 GET 请求方式。根据请求中的用户 ID 列表批量删除用户记录。

    :param request: Django 的 HttpRequest 对象，包含请求的相关信息。
    :return: JsonResponse 对象，包含操作结果的状态码、消息和数据。
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "data": {}}
        req_dict = request.session.get("req_dict")

        # 调用 users 模型的 deletes 方法，传入模型自身、模型自身以及请求数据中的用户 ID 列表，执行删除操作
        error = users.deletes(users,
            users,
            req_dict.get("ids")
        )
        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return JsonResponse(msg)
