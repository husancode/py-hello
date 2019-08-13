class Student(object):
    __slots__ = ('name','__age','show_age')
    city='hangzhou'
    def __init__(self):
        self.name = 'husan'
        self.__age = 25
    def hello(self):
        print(self.__age)
    def bingo(self):
        print('bingboi')
def show_age(self):
    print(self.name)
def say(self):
    self.hello()
from types import MethodType
s = Student()
s.show_age = MethodType(show_age, s)
s.show_age()
s.hello()
Student.say = say
s.say()
s.bingo()
