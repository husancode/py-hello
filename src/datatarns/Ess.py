import struct

def checkBmp(path):
    with open(path,mode='rb') as f:
        buffer = f.read(2)
        flag = struct.unpack('<cc', buffer)
        if(flag[0]==b'B' and flag[1]==b'M'):
            return True
        return False
print(checkBmp('D:\\111.bmp'))
print(checkBmp('D:\\tt.png'))

import hashlib

sha1 = hashlib.sha1()
sha1.update(b'how to use sha1 in ')
print(sha1.hexdigest())
