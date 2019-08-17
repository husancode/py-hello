#清理客户关联设备和物品等区域信息
import pymysql
import logging
logging.basicConfig(level=logging.INFO)

conn = pymysql.connect(host='192.168.50.178', user = "root", passwd="123456", db="equipment-20190810", port=3306, charset="utf8")
cur = conn.cursor()

sql = r"SELECT id,division_id,addr_name,addr_detail,division_id_old,addr_name_old FROM t_install_customer WHERE division_id_old IS NOT NULL "
cur.execute(sql)
customers = cur.fetchall()
print("customers:", len(customers))
for customer in customers:
    ## 更新客户关联设备信息
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

    ## 更新客户关联物品信息
    sql2 = r"select id from deposit_info where unit_id='{}'".format(customer[0])
    cur.execute(sql2)
    depositRows = cur.fetchall()
    if(depositRows and len(depositRows)> 0):
        ids = ",".join(map(lambda x: "'"+x[0]+"'", depositRows))
        sql2 = r"update deposit_info set division_id='{}' where id in ({})".format(customer[1], ids)
        logging.info(sql2)
        cur.execute(sql2)
        sql2 = r"update deposit_info_ext set addr_name='{}', addr_detail='{}',update_date=now() where id in ({})".format(customer[2], customer[3], ids)
        logging.info(sql2)
        cur.execute(sql2)

    ## 更新t_check_task_crm信息
    sql3 = r"update t_check_task_crm set crm_addr_name='{}',crm_addr_detail='{}',update_date=now() where crm_id='{}'".format(customer[2], customer[3], customer[0])
    cur.execute(sql3)

cur.close()
conn.commit()
conn.close()