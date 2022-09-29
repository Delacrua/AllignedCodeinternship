import threading
import socket

ADMINS = {'admin': hash('adminpass')}
HOST = '127.0.0.1'
PORT = 52525


class TCPChatServer:

    def __init__(self, host=HOST, port=PORT, sock=None):
        self.host = host
        self.port = port
        self.clients = {}
        if sock is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except Exception:
                nickname = self.clients[client]
                self.clients.pop(client)
                client.close()
                self.broadcast(f'{nickname} left the chat'.encode('utf-8'))
                break

    def receive(self):
        while True:
            client, address = self.socket.accept()
            print(f'Connected with {str(address)}')

            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            if nickname in ADMINS:
                client.send('PASS'.encode('utf-8'))
                password = client.recv(1024).decode('utf-8')
                if hash(password) != ADMINS[nickname]:
                    client.send('REFUSE'.encode('utf-8'))
                    client.close()
                    continue
            self.clients[client] = nickname

            print(f'Nickname of the client is {nickname}')
            self.broadcast(f'{nickname} joined the chat'.encode('utf-8'))
            client.send('connected to the server'.encode('utf-8'))

            thread = threading.Thread(target=self.handle, args=(client, ))
            thread.start()


def main():
    server = TCPChatServer()
    server.run_server()
    server.receive()


if __name__ == '__main__':
    print('The TCP server is listening')
    main()
