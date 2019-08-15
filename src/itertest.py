import itertools
import time
for x in itertools.imap(lambda x, y: x * y, [10, 20, 30], itertools.count(1)):
    print(x)