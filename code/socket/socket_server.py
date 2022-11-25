import socket
from _thread import *

client_sockets = []  # 서버에 접속한 클라이언트 목록

# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리


def threaded(client_socket, addr):
    print('>> Connected by :', addr[0], ':', addr[1])

    # 클라이언트가 접속을 끊을 때 까지 반복합니다.

    try:
        result = 'T'

        # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
        user = client_socket.recv(1024).decode('utf-8')

        client_socket.send(result.encode('utf-8'))

        print('user 값 recv : ', user)
        print('result 값 send : ', result)

        # 서버에 접속한 클라이언트들에게 채팅 보내기
        # 메세지를 보낸 본인을 제외한 서버에 접속한 클라이언트에게 메세지 보내기

    except ConnectionResetError as e:
        print('>> Disconnected by ' + addr[0], ':', addr[1])

    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print('remove client list : ', len(client_sockets))

    client_socket.close()

# 서버 IP 및 열어줄 포트


def socket_server():

    HOST = '192.168.137.5'
    PORT = 9999

    # 서버 소켓 생성
    print('>> Server Start')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    try:
        while True:
            print('>> Wait')

            (client_socket, addr) = server_socket.accept()
            client_sockets.append(client_socket)
            start_new_thread(threaded, (client_socket, addr))
            print("참가자 수 : ", len(client_sockets))

    except Exception as e:
        print('에러는? : ', e)

    finally:
        server_socket.close()


socket_server()

# 쓰레드에서 실행되는 코드입니다.
# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다.
