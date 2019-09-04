import pymysql
import random

import uuid
def getUUID():
    return "".join(str(uuid.uuid4()).split("-"))

print(getUUID())