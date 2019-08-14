class Zone(object):
    def __init__(self, name):
        self.name = name

def fn(self, name):
    self.name = name
    print('Hello,%s' % name)
Hello = type('Hello', (object,), dict(hello=fn))
print(type(Hello))
s = Hello()
s.hello('husan')