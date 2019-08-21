from collections import namedtuple
import psutil
import time

def statRemoteTcp(url, port):
    """
    与远程url,port的连接状态统计
    :param url:
    :param port:
    :return:
    """
    count_dict = dict()
    netstat = psutil.net_connections()
    for peer in netstat:
        if(hasattr(peer.raddr, 'ip')):
            if (peer.raddr.ip == url and peer.raddr.port == port):
                if peer.status in count_dict:
                    count_dict[peer.status] += 1
                else:
                    count_dict[peer.status] = 1
    return count_dict

def statLocalTcp(port):
    """
        本地port的连接状态统计
        :param url:
        :param port:
        :return:
        """
    count_dict = dict()
    netstat = psutil.net_connections()
    for peer in netstat:
        if (hasattr(peer.laddr, 'ip')):
            if (peer.laddr.port == port):
                print(peer)
                if peer.status in count_dict:
                    count_dict[peer.status] += 1
                else:
                    count_dict[peer.status] = 1
    return count_dict

def statTcpStatus():
    """
    统计本机连接状态
    :return:
    """
    count_dict = dict()
    netstat = psutil.net_connections()
    for peer in netstat:
        if peer.status in count_dict:
            count_dict[peer.status] += 1
        else:
            count_dict[peer.status] = 1
    return count_dict

print(statTcpStatus())


def test():
    while(True):
        print(statRemoteTcp('192.168.50.178',3306))
        time.sleep(3)

