#import Test
import struct
COM_QUIT = 0x01

send_data = struct.pack('<iB', 1, COM_QUIT)
print(send_data)