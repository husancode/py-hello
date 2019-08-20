from mysqlUtil import tableUtil
import time

now = time.time()
tableUtil.clearDivision()

print('cost time: %s' % (time.time()-now))
