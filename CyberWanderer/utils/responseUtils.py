"""
    统一返回体
"""

from django.http import JsonResponse


# 自定义状态码
class HttpCode(object):
    # 正常登陆
    ok = 200
    # 参数错误
    paramsError = 400
    # 权限错误
    unauth = 401
    # 方法错误
    methodError = 405
    # 服务器内部错误
    servererror = 500


# 定义统一的 json 字符串返回格式
def result(code=HttpCode.ok, message="", data=None, kwargs=None):
    json_dict = {"code": code, "message": message, "data": data}
    # isinstance(object对象, 类型):判断是否数据xx类型
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)


# 成功
def ok(message="", data=None):
    return result(code=HttpCode.ok, message=message, data=data)


# 参数错误
def params_error(message="", data=None):
    return result(code=HttpCode.paramsError, message=message, data=data)


# 权限错误
def unauth(message="", data=None):
    return result(code=HttpCode.unauth, message=message, data=data)


# 方法错误
def method_error(message="", data=None):
    return result(code=HttpCode.methodError, message=message, data=data)


# 服务器内部错误
def server_error(message="", data=None):
    return result(code=HttpCode.servererror, message=message, data=data)
