import socket
import threading

HOST = '127.0.0.1'
PORT = 52525


class TCPChatClient:
    stop = False

    def __init__(self, host=HOST, port=PORT, sock=None):
        self.host = host
        self.port = port
        self.nickname = input('Choose a nickname: ')
        if self.nickname == 'admin':
            self.password = input('Input admin password: ')
        if sock is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self):
        while True:
            if self.stop:
                break
            message = f'{self.nickname}: {input("")}'
            self.socket.send(message.encode('utf-8'))

    def receive(self):
        while True:
            if self.stop:
                break
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.socket.send(self.nickname.encode('utf-8'))
                    new_message = self.socket.recv(1024).decode('utf-8')
                    if new_message == 'PASS':
                        self.socket.send(self.password.encode('utf-8'))
                        if self.socket.recv(1024).decode('utf-8') == 'REFUSE':
                            print('Connection refused. Wrong password.')
                            self.stop = True
                    elif new_message == 'BAN':
                        print('Connection refused. Banned nickname.')
                        self.socket.close()
                        self.stop = True
                else:
                    print(message)
            except Exception as exc:
                print(f'An error occurred: {exc}')
                break

    def connect_to_server(self):
        self.socket.connect((self.host, self.port))
        receive_thread = threading.Thread(target=self.receive)
        write_thread = threading.Thread(target=self.send_message)
        receive_thread.start()
        write_thread.start()


def main():
    client = TCPChatClient()
    client.connect_to_server()


if __name__ == '__main__':
    main()
