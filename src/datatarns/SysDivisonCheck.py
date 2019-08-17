#清洗t_sys_divisioin表坐标数据
import pymysql
import uuid

def getUUID():
    return "".join(str(uuid.uuid4()).split("-"))
print(getUUID())

conn = pymysql.connect(host='192.168.50.178', user = "root", passwd="123456", db="equipment-20190810", port=3306, charset="utf8")
cur = conn.cursor()
cur.execute(r"SELECT id FROM t_sys_division  WHERE `name`='西湖区'")
rootDivisionId = cur.fetchone()[0]
print(rootDivisionId)

def getName(sysMap, v, root):
    name=''
    division = v
    while(True):
        aName = division[1]
        parentId = division[3]
        name = '->'+aName+name
        id = division[0]
        if(id == root):
            break
        division = sysMap[parentId]
    name = name[2:]
    return name

def getByName(nameMap, name):
    result = []
    name = name.split("->")
    newName = name.pop()
    newId = getUUID()
    result.append(newId)
    result.append(newName)
    parentName = "->".join(name)
    if parentName in nameMap:
        division = nameMap[parentName]
        newParentId = division[0]
        result.append(newParentId)
        newParentIds = division[4]+','+newParentId
        result.append(newParentIds)
        print(result)
        return result
    else:
        pass

def comp(key):
    name = key[1].split("->")
    return len(name)

divisionSql = r"SELECT * FROM t_sys_division WHERE parent_ids LIKE '%{}%' OR id='{}'".format(rootDivisionId, rootDivisionId)
cur.execute(divisionSql)
sysMap = {}
nameMap = {}
xihuDivisions = cur.fetchall()
for xihuDivision in xihuDivisions:
    sysMap[xihuDivision[0]]=xihuDivision
for k,v in sysMap.items():
    name = getName(sysMap, v, rootDivisionId)
    nameMap[name] = v


sql = r"select id,name from zone "
cur.execute(sql)
ret = cur.fetchall()
ret2 = sorted(ret, key=comp)
print(ret2)
for row in ret2:
    name = row[1]
    if name in nameMap:
        division = nameMap[name]
        updateSql = r"update zone set division_id='{}' where id={}".format(division[0], row[0])
        cur.execute(updateSql)
    else:
        newDivision = getByName(nameMap, name)
        if(newDivision != None):
            insertSql = r"INSERT INTO `t_sys_division` (`id`,`name`,`alias_name`,`parent_id`,`parent_ids`,`level`,`coords`," \
                        r"`zoom`,`user_id`,`emap_type`,`create_by`,`create_date`,`del_flag`) " \
                        r"VALUES('{}','{}','{}','{}','{}',4,'',0,NULL,1,'husan',NOW(),0)".format(newDivision[0], newDivision[1], newDivision[1],
                                                                                                 newDivision[2],newDivision[3])
            print(cur.execute(insertSql))
            updateSql = r"update zone set division_id='{}' where id={}".format(newDivision[0], row[0])
            print(cur.execute(updateSql))

cur.close()
conn.commit()
conn.close()
