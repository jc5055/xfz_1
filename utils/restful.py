from django.http import JsonResponse


class HttpCode(object):
    ok = 200
    paramserror = 400
    unautherror = 401
    methoderror = 405
    servererror = 500


def result(code=HttpCode.ok, message="", data={}, kwargs=None):
    json_dict = {"code": code, "message": message, "data": data}
    if kwargs and isinstance(kwargs, dict) and kwargs.key():
        json_dict.update(kwargs)

    return JsonResponse(json_dict)


def ok(message="", data={}):
    return result()


def paramserror(message="", data={}):
    return result(code=HttpCode.paramserror, message=message, data=data)


def unautherror(message="", data={}):
    return result(code=HttpCode.unautherror, message=message, data=data)


def methoderror(message="", data={}):
    return result(code=HttpCode.methoderror, message=message, data=data)


def servererror(message="", data={}):
    return result(code=HttpCode.servererror, message=message, data=data)
