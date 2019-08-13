from FuncDef import record
from FuncDef import calc
from FuncDef import *
from collections.abc import Iterable
from collections.abc import Iterator
from functools import reduce
import datetime

a =(1,2,3,4)
print(isinstance(a, Iterable))
print(isinstance(a, Iterator))
#calc(*a)
extra = {'city':'hanghzou', 'like':'asdf'}
print(sum(a))
ac = reduce(fn, a)
print(ac)

print(int('123'))

a = lambda x:x*x
print(a)
ac = map(a, list(range(10)))
print(ac)
print(list(ac))

#装饰器
def log(func):
    def wrapper(*args, **kw):
        print('call {}():args:{},kw:{}'.format(func.__name__,args,kw))
        return func(*args, **kw)
    return wrapper
@log
def now(*args, **kw):
    print((datetime.datetime.now()))
f = now
a =(1,2,3,4)
dc = {'ac':'aa','ab':1}
f(a, **dc)

#person('husan',33, **extra)

#person('Jack', 24, city='Beijing', addr='Chaoyang', zipcode=123456)

#person1('hhh',11,job='compute')

#teacher('hhh',11,2,3,job='compute',city='hz')

#per('husan', 33, **extra)
#print(extra)