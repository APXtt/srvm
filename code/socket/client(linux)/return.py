import socket
import time
from _thread import *


req = 'return'  # 반납
user = 'usersssss'  # user id
pd_name = 'smartphone'  # 상품명


def socket_client():

    HOST = '220.67.3.173'
    PORT = 1234

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((HOST, PORT))

    s.send(req.encode('utf-8'))
    time.sleep(2)

    s.send(user.encode('utf-8'))
    time.sleep(1)

    s.send(pd_name.encode('utf-8'))

    result = s.recv(1024).decode('utf-8')
    print(result)


socket_client()
