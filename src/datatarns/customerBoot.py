## 客户区域信息清理
#print('开始初始化zone坐标！')
#import ZoneGisCheck
#print('Zone坐标初始化完成！')
print('t_sys_division数据初始化')
import SysDivisonCheck
SysDivisonCheck.transData()
SysDivisonCheck.transData()
print('t_sys_division数据初始化完成')

print('客户区域信息初始化开始')
import  CustomerTrans
CustomerTrans.transData()
print('客户区域信息初始化完成')

print('客户关联设备，物品，检查记录初始化')
import customerLink
print('客户关联设备，物品，检查记录初始化完成')

