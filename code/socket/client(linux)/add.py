import socket
import time
from _thread import *


req = 'add'  # 추가
pd_name = 'smartphone'


def socket_client():

    HOST = '220.67.3.173'
    PORT = 1234

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((HOST, PORT))

    s.send(req.encode('utf-8'))
    time.sleep(1)

    s.send(pd_name.encode('utf-8'))

    result = s.recv(1024).decode('utf-8')
    print(result)


socket_client()
