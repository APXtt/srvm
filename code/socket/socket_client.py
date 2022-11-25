import socket
from _thread import *

user = 'abc'

# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리


def socket_client():

    HOST = '192.168.137.5'
    PORT = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    client_socket.send(user.encode('utf-8'))

    result = client_socket.recv(1024).decode('utf-8')

    print('user 값 send : ', user)
    print('result 값 recv : ', result)

    client_socket.close()


socket_client()
