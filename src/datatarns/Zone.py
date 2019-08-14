# 更新zone位置数据（标准化）
import pymysql
conn = pymysql.connect(host='192.168.50.178', user = "root", passwd="123456", db="equipment-20190810", port=3306, charset="utf8")
cur = conn.cursor()
#获取数据
n = 1
while(n<1000):
    sql = r"update zone set amap_polygongeo_u=ST_GeomFromText(polygongeo) where id={}".format(n)
    try:
        r =cur.execute(sql)
        print(r)
    except Exception as e:
        print('Error:', e)
    finally:
        pass
    n=n+1

cur.close()
conn.close()
