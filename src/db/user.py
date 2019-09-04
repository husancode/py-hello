#encoding: utf-8
"""
@Auther: husan
@Date: 2019/9/4 13:17

"""

import pymysql
import time
import random

def createTable():
    conn = pymysql.connect(host='127.0.0.1', user="root", passwd="123456", db="auth", port=3306,
                           charset="utf8")
    cur = conn.cursor()
    sql = """CREATE TABLE `t_app_users` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL COMMENT '用户名',
  `mobile` varchar(16) DEFAULT NULL COMMENT '手机号',
  `email` varchar(32) DEFAULT NULL COMMENT '邮箱',
  `password` varchar(64) DEFAULT NULL COMMENT '密码',
  `uuid` varchar(64) DEFAULT NULL COMMENT '客户端唯一标识号',
  `push_token` varchar(64) DEFAULT NULL COMMENT '推送的令牌',
  `sex` tinyint(4) DEFAULT NULL COMMENT '性别(0->男, 1->女)',
  `source` int(2) DEFAULT NULL COMMENT '用户注册来源(0->iPhone, 1->iPad, 2->Android, 3->微信, 4->H5, 5->网站)',
  `avatar` varchar(128) DEFAULT NULL COMMENT '头像',
  `position` varchar(32) DEFAULT NULL COMMENT '经度',
  `addr_detail` varchar(200) DEFAULT NULL COMMENT '详细地址',
  `status` int(2) DEFAULT '1' COMMENT '状态',
  `create_date` timestamp NULL DEFAULT NULL,
  `update_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`) USING BTREE,
  FULLTEXT KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=31818015 DEFAULT CHARSET=utf8mb4 COMMENT='APP用户表'"""""
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def data_init(batch=2000, total=1000000000):
    try:
        conn = pymysql.connect(host='127.0.0.1', user="root", passwd="123456", db="auth", port=3306,
                               charset="utf8")
        cur = conn.cursor()
        start = time.time()
        sql = r"insert into t_app_users(`name`,`mobile`,`email`,`password`,`uuid`,`push_token`,`sex`,`status`) values "
        num = 0
        while(num < total):
            count = min(batch, (total-num))
            insert_data = generate(count)
            sql_sufix = ",".join(map(str, insert_data))
            insert_sql = sql + sql_sufix
            print('insert {}'.format(count))
            cur.execute(insert_sql)
            conn.commit()
            num = num + count
    finally:
        end = time.time()
        print('cost time {}'.format((end-start)))
        cur.close()
        conn.close()



def generate(count):
    i = 0
    data = []
    while(i < count):
        data.append(generate_data())
        i = i + 1
    return data

import uuid
def getUUID():
    return "".join(str(uuid.uuid4()).split("-"))

def generate_data():
    name = "".join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJ', 12))
    mobile = "".join(random.sample('123456789123456789', 11))
    email = "".join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJ', 10))
    pwd = "".join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJ', 32))
    uuid = getUUID()
    push_token = getUUID()
    sex = random.randrange(0, 2)
    status = random.randrange(0, 2)
    r = (name, mobile, email, pwd, uuid, push_token, sex, status)
    return r

data_init()