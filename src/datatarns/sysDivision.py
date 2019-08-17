from mysqlUtil import tableUtil
import time

now = time.time()
divisons = tableUtil.clearDivision()
print('cost time: %s' % (time.time()-now))
