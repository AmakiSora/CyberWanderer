"""
    多线程工具
"""

import threading

"""
    多线程处理数组(数组arrayList,处理函数function,函数的参数params,线程数)
    注意事项:
        1.处理函数的第一个参数一定要为数据,且函数的参数params里不传第一个参数,其他参数要按照顺序传元组(只有一个参数则不填)
        2.处理函数返回值只能有一个
        3.本函数有两个返回值,
            第一个返回值为0表示数组为空,为200表示成功,
            第二个返回值是statusInfo,可以对数据进行统计
        4.statusInfo为字典,里面的参数可自定义,需要函数返回key,value
            如果key为None,无事发生
            如果key不为空
                value为空,且key原本不存在,value默认为1
                value为空,且key原本存在,且value为int,value += 1
                value不为空,则新增或修改该key,值为value
"""


def multithreading_list(arrayList, function, params=None, thread_num=0):
    statusInfo = {}
    count = len(arrayList)
    statusInfo['count'] = count
    if thread_num == 0:
        if count > 1000:
            thread_num = 50
        elif count > 500:
            thread_num = 30
        elif count > 100:
            thread_num = 10
        elif count > 20:
            thread_num = 5
        elif count > 5:
            thread_num = 3
        elif count > 0:
            thread_num = 2
        else:
            return 0, statusInfo
    threads = []
    loopFunctionParams = (arrayList, statusInfo, function, params)
    for i in range(thread_num):
        threads.append(threading.Thread(target=loopFunction, args=loopFunctionParams))
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    return 200, statusInfo


# 循环处理数组
def loopFunction(*loopFunctionParams):
    try:
        arrayList = loopFunctionParams[0]
        statusInfo = loopFunctionParams[1]
        function = loopFunctionParams[2]
        params = loopFunctionParams[3]
        data = arrayList.pop()
        while data is not None:
            if params is None:
                finalParams = [data]
            else:
                finalParams = [data, *params]
            key, value = function(*finalParams)
            if key is None:
                continue
            if value:
                statusInfo[key] = value
            else:
                if not statusInfo.get(key):
                    statusInfo[key] = 0
                if type(statusInfo[key]) is int:
                    statusInfo[key] += 1
            data = arrayList.pop()
    except:
        return
