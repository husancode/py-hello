import functools

@functools.lru_cache(100)
def cal(num):
    i = 0
    result = 1
    while(True):
        i+=1
        if i > num:
            break
        result = result*2
    print(result)
    return result

a = cal(4)
b = cal(4)
