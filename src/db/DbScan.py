
#encoding: utf-8
"""
@Auther: husan
@Date: 2019/9/7 10:54

"""

import pymysql
import time


def sccan():
    conn = pymysql.connect(host='127.0.0.1', user="root", passwd="123456", db="auth", port=3306,
                               charset="utf8")
    cur = conn.cursor()
    id = 25000000
    sql = r" SELECT * FROM t_app_users  where id>{} order by id asc limit 0,2000 ".format(id)
    s1 = time.time()
    cur.execute(sql)
    print((time.time()-s1))
    rows = cur.fetchall()
    while(rows):
        id = rows[-1][0]
        print(id)
        sql = r" SELECT * FROM t_app_users  where id>{} order by id asc limit 0,2000 ".format(id)
        statr = time.time()
        cur.execute(sql)
        rows = cur.fetchall()
        print(time.time()-statr)
    print('cost time :', (time.time()-s1))

def sscan():
    conn = pymysql.connect(host='127.0.0.1', user="root", passwd="123456", db="auth", port=3306,
                           charset="utf8")
    cur = pymysql.cursors.SSCursor(conn)
    sql = r"select * from t_app_users"
    s1 = time.time()
    cur.execute(sql)
    print(time.time()-s1)
    while(True):
        s2 = time.time()
        rows = cur.fetchmany(2000)
        print(rows[-1][0])
        print(time.time()-s2)
        if not rows:
            break
    print('cost time:', str(time.time()-s1))
    conn.close()

sscan()



