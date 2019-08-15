#清理客户关联设备和物品区域信息
import pymysql
import logging
logging.basicConfig(level=logging.INFO)

conn = pymysql.connect(host='192.168.50.178', user = "root", passwd="123456", db="equipment-20190810", port=3306, charset="utf8")
cur = conn.cursor()

sql = r"SELECT id,division_id,addr_name,addr_detail,division_id_old,addr_name_old FROM t_install_customer WHERE division_id_old IS NOT NULL "
cur.execute(sql)
customers = cur.fetchall()
for customer in customers:
    sql = """SELECT
		t.device_id as 'deviceId',
		t.addr_name as 'addrName',
		t.addr_detail as 'addrDetail',
		r.build_id as 'buildId',
		r.floor
		from v_nb_dtu_model t
		left join t_install_record r on r.sn=t.serial_no
		where r.customer_id='{}'""".format(customer[0])
    cur.execute(sql)
    devices = cur.fetchall()
    for device in devices:
        sql = """update t_nb_dtu_info set
            addr_name='{}',addr_detail='{}',division_id='{}',update_date=now()
        where device_id='{}'""".format(customer[2],customer[3],customer[1], device[0])
        cur.execute(sql)

    sql2 = r"update deposit_info set division_id='{}' where unit_id='{}' ".format(customer[1], customer[0])
    cur.execute(sql2)

cur.close()
conn.commit()
conn.close()