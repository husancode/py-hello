#encoding: utf-8
"""
@Auther: husan
@Date: 2019/8/23 15:11

"""
import functools
import time

lastInvokeDict = {}

def limit(interval):
    """
    限流装饰器
    :param interval:millisecond
    :return:
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            funcName = func.__name__
            if funcName in lastInvokeDict:
                lastInvoke = lastInvokeDict[funcName]

                escape = (time.time_ns()-lastInvoke)//1000000
                while escape < interval:
                    time.sleep((interval-escape) /1000)
                    escape = (time.time_ns()-lastInvoke)//1000000
            else :
                pass
            now = time.time_ns()
            lastInvokeDict[funcName] = now
            print('invoke:', now/1000000)
            return func(*args, **kw)
        return wrapper
    return decorator
