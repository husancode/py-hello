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
        if (hasattr(peer.laddr, 'port')):
            if (peer.laddr.port == port):
                print(peer)
                if peer.status in count_dict:
                    count_dict[peer.status] += 1
                else:
                    count_dict[peer.status] = 1
    return count_dict

def statTcp(*args):
    netstat = psutil.net_connections()
    for peer in netstat:
        for arg in args:
            if(test(peer, arg)):
                print(peer)
                break


def test(peer, ipPort):
    if(len(ipPort) == 1):
        port = ipPort[0]
        if (hasattr(peer.laddr, 'port')):
            if (peer.laddr.port == port):
                return True
    elif(len(ipPort) >= 2):
        port = ipPort[0]
        ip = ipPort[1]
        if (hasattr(peer.raddr, 'ip')):
            if (peer.raddr.ip == ip and peer.raddr.port == port):
                return True
    return False




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

def printTcp(status=None, port=None):
    """
    打印符合条件的连接
    :param status:
    :return:
    """
    netstat = psutil.net_connections()
    for peer in netstat:
        if status :
            if(peer.status == status):
                print(peer)
                continue
        if port:
            if((hasattr(peer.laddr, 'port') and peer.laddr.port == port) or (hasattr(peer.raddr, 'port') and peer.raddr.port == port)):
                print(peer)
                continue

statTcp((3306,),(3306,'::1'))

def test():
    while(True):
        print(statRemoteTcp('192.168.50.178',3306))
        time.sleep(3)

