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
print(psutil.cpu_times())
print(psutil.virtual_memory())
print(psutil.swap_memory())
print(psutil.disk_usage('E:\workspace\equipment-platform'))
print(psutil.disk_partitions())
print(psutil.disk_io_counters())