from collections import namedtuple
import psutil
import time

def printProcess(*pid):
    pids = psutil.pids()
    for aPid in pid:
        if aPid in pids:
            p = psutil.Process(aPid)
            print(p.cmdline())
            print(p.connections())
            print(p.cpu_percent())
            print(p.cpu_times)
            print(p.exe())
            print(p.threads())
            print(p)


# for i in range(2):
#     print(psutil.cpu_percent(interval=2))
#
# for i in range(100):
#     print(psutil.disk_io_counters())
#     time.sleep(1)
def diskShow(path):
    data = psutil.disk_usage('C:\Program Files\mysql-5.7.21-winx64\data')
    print(type(data))

def diskStat(count):
    last = 0
    i = 0
    while(i < count):
        writes = psutil.disk_io_counters().write_bytes
        if(last > 0):
            print((writes-last)/1024/1024)
        last = writes
        i = i + 1
        time.sleep(1)

diskStat(100)
