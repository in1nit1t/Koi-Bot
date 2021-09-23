import requests
import traceback
from functools import wraps

from core.logger import logger


class Decorator:

    # CQHTTP API FETCH DECORATOR
    @staticmethod
    def cqhttp_api(api_name):
        def fetch_decorator(func):
            @wraps(func)
            def wrapped_function(*args):
                params = func(*args) if args else func()
                try:
                    url = "http://127.0.0.1:5700/" + api_name
                    response = requests.get(url=url, params=params).json()
                except:
                    logger.error(f"<CQHTTP API> 调用 /{api_name}/ 失败", traceback.format_exc())
                    return False

                # STATUS OK
                if response["status"] == "ok":
                    return response["data"]
                return dict()
            return wrapped_function
        return fetch_decorator

    # ALAPI FETCH DECORATOR
    @staticmethod
    def alapi_fetch(api_name, field=''):
        def fetch_decorator(func):
            @wraps(func)
            def wrapped_function(*args):
                params = func(*args) if args else func()
                try:
                    url = "https://v2.alapi.cn/api/" + api_name
                    response = requests.get(url=url, params=params).json()
                except:
                    logger.error(f"<ALAPI> 调用 /{api_name}/ 失败", traceback.format_exc())
                    return False

                # ERROR CODE 200 MEANS SUCCESS
                if response["code"] == 200:
                    return response["data"][field] if field else response["data"]

                # API INTERFACE ERROR
                error_map = {
                    100: "token 错误",
                    101: "账号过期",
                    102: "接口请求次数超过限制",
                    104: "来源或 ip 不在白名单",
                    400: "接口请求失败",
                    404: "接口地址不存在",
                    405: "请求方法不被允许",
                    406: "没有更多数据了",
                    422: "接口请求失败",
                    429: "技能 CD 中"
                }
                logger.error(f"<ALAPI> /{api_name}/ 接口返回异常", error_map[response["code"]])
                return dict()
            return wrapped_function
        return fetch_decorator

    # BILIBILI API FETCH DECORATOR
    @staticmethod
    def bilibili_fetch(url):
        def fetch_decorator(func):
            @wraps(func)
            def wrapped_function(*args):
                params = func(*args) if args else func()
                try:
                    response = requests.get(url=url, params=params).json()
                except:
                    logger.error(f"<Bilibili API> 调用 [{url}] 失败", traceback.format_exc())
                    return False

                # ERROR CODE 0 MEANS SUCCESS
                error_code = response["code"]
                if error_code == 0:
                    return response["data"]

                logger.error(f"<Bilibili API> [{url}] 接口返回异常", response['message'])
                return dict()
            return wrapped_function
        return fetch_decorator

    # ROLLBACK ON INSERT ERROR
    @staticmethod
    def db_insert(func):
        @wraps(func)
        def try_except(*args):
            try:
                func(*args)
                args[0].connect.commit()
                return args[0].cursor.lastrowid
            except:
                logger.error(f"<MySQL> 插入失败", traceback.format_exc())
                args[0].connect.rollback()
                return 0
        return try_except

    # ROLLBACK ON MODIFY ERROR
    @staticmethod
    def db_modify(func):
        @wraps(func)
        def try_except(*args):
            try:
                func(*args)
                args[0].connect.commit()
                return True
            except:
                logger.error(f"<MySQL> 更新/删除失败", traceback.format_exc())
                args[0].connect.rollback()
                return False
        return try_except

    # RETURN NULL ON SELECT ERROR
    @staticmethod
    def db_select_one(func):
        @wraps(func)
        def try_except(*args):
            try:
                func(*args)
                return args[0].cursor.fetchone()
            except:
                logger.error(f"<MySQL> 查询失败", traceback.format_exc())
                return tuple()
        return try_except

    # RETURN NULL ON SELECT ERROR
    @staticmethod
    def db_select_all(func):
        @wraps(func)
        def try_except(*args):
            try:
                func(*args)
                return args[0].cursor.fetchall()
            except:
                logger.error(f"<MySQL> 查询失败", traceback.format_exc())
                return tuple()
        return try_except
