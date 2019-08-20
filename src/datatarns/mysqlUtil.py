import pymysql
from config import DB
def connInit():
    conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3], port=DB[4], charset="utf8")
    return conn

def getTables(ignore):
    """
    返回数据库所有的表（不包含视图）
    :param ignore:排除某些表
    :return:
    """
    showTables = r"show tables"
    conn = connInit()
    cur = conn.cursor()
    cur.execute(showTables)
    tables = cur.fetchall()
    cur.close()
    conn.close()
    result = []
    for table in tables:
        if(not table[0].startswith('v_')):
            result.append(table[0])
    return list(set(result).difference(ignore))

def testTable(table, *field):
    """
    返回包含field字段的表
    :param table:
    :param field:
    :return:
    """
    showColumns = r"desc {}".format(table)
    conn = connInit()
    cur = conn.cursor()
    cur.execute(showColumns)
    columns = cur.fetchall()
    cur.close()
    conn.close()
    for f in field:
        found = False
        for column in columns:
            if(f == column[0]):
                return True
        if(found == False):
            return False
    return True

def tableScan(ignore, *field):
    tables = getTables(ignore)
    divisionIdList = []
    for table in tables:
        if(testTable(table,*field)):
            divisionIdList.append(table)
    return divisionIdList

class tableUtil(object):
    _ignore = set(['zone','t_install_customer_2019','t_amap_basics','ess_station_area_ref','t_amap_division','ess_plan_area','stat_area_customer','stat_area_sensor'])
    _root = None
    _tables = None

    @classmethod
    def scanTables(cls):
        if(not cls._tables):
            cls._tables = tableScan(cls._ignore,'division_id')
        return cls._tables

    @classmethod
    def getRootdivision(cls):
        """
        :return: 返回西湖区节点id
        """
        if(not cls._root):
            conn = connInit()
            cur = conn.cursor()
            cur.execute(r"SELECT id FROM t_sys_division  WHERE `name`='西湖区'")
            cls._root = cur.fetchone()[0]
            conn.close()
        return cls._root

    @classmethod
    def scanSysDivision(cls, level=3):
        """
        返回西湖区下面level=3以下级别的记录，后面进行清理
        :param level:
        :return:[id,parentIds,name]
        """
        root = cls.getRootdivision()
        conn = connInit()
        cur = conn.cursor()
        cur.execute(r"SELECT id,parent_ids,NAME FROM t_sys_division WHERE parent_ids LIKE '%{}%' AND create_by!='husan'".format(root))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        sep = root+','
        result = []
        for row in rows:
            divisionSep = row[1].split(sep)
            if(len(divisionSep) >=2):
                divisionArr = divisionSep[1].split(",")
                if(len(divisionArr) >=level):
                    result.append(row)
        return result

    @classmethod
    def checkDivision(cls, division):
        """
        检查是表是否有关联division
        :param division:
        :return:
        """
        tables = cls.scanTables()
        flag = True
        for table in tables:
            sql = r"select 1 from {} where division_id='{}' limit 0,1".format(table, division[0])
            conn = connInit()
            cur = conn.cursor()
            cur.execute(sql)
            row = cur.fetchone()
            cur.close()
            conn.close()
            if row:
                print('table {} exist division_id:{},name:{}'.format(table, division[0], division[2]))
                flag = False
                break
        return flag

    @classmethod
    def getCandeleteDivision(cls, level=3):
        """
        返回可以被删除的t_sys_divisions记录
        :return:
        """
        result = []
        divisions = cls.scanSysDivision(level)
        print
        for division in divisions:
            flag = cls.checkDivision(division)
            if flag:
                result.append(division)
        return result

    @classmethod
    def clearDivision(cls):
        divisions = cls.getCandeleteDivision()
        if(not divisions):
            return
        ids = ",".join(map(lambda x: "'"+x[0]+"'", divisions))
        sql = r"select * from t_sys_division where id in({})".format(ids)
        conn = connInit()
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        sql = r"CREATE  TABLE IF NOT EXISTS t_sys_division_bak (LIKE t_sys_division)"
        cur.execute(sql)
        sql = r"INSERT INTO t_sys_division_bak SELECT * FROM t_sys_division WHERE id IN({})".format(ids)
        cur.execute(sql)
        conn.commit()
        sql = r"delete from t_sys_division  where id in({})".format(ids)
        cur.execute(sql)
        conn.commit()











