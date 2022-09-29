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
        self.nicknames = {}
        self.banned_users = set()
        if sock is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def kick_user(self, nickname_to_kick):
        if nickname_to_kick in self.nicknames:
            client_to_kick = self.nicknames[nickname_to_kick]
            print(f'{nickname_to_kick} was kicked')
            self.broadcast(
                f'{nickname_to_kick} was kicked by the admin'.encode('utf-8'))
            self.clients.pop(client_to_kick)
            self.nicknames.pop(nickname_to_kick)
            client_to_kick.close()

    def ban_user(self, nickname_to_ban):
        self.banned_users.add(nickname_to_ban)
        print(f'{nickname_to_ban} was banned')
        self.broadcast(f'{nickname_to_ban} '
                       f'was banned by the admin'.encode('utf-8'))

    def handle(self, client):
        nickname = self.clients[client]
        while True:
            try:
                message = client.recv(1024)
                msg = message.decode('utf-8').strip()[len(nickname) + 2:]

                if msg.startswith('/kick'):
                    if nickname in ADMINS:
                        name_to_kick = msg[6:]
                        self.kick_user(name_to_kick)
                    else:
                        client.send('Only admin can kick users'.encode('utf-8')
                                    )

                elif msg.startswith('/ban'):
                    if nickname in ADMINS:
                        name_to_ban = msg[5:]
                        self.kick_user(name_to_ban)
                        self.ban_user(name_to_ban)
                    else:
                        client.send('Only admin can ban users'.encode('utf-8'))
                else:
                    self.broadcast(message)

            except ConnectionAbortedError:
                self.broadcast(f'{nickname} left the chat'.encode('utf-8'))
                break

            except Exception as exc:
                self.clients.pop(client)
                self.nicknames.pop(nickname)
                print(f'client with nickname "{nickname}" '
                      f'removed after error: {exc}')
                self.broadcast(f'{nickname} left the chat'.encode('utf-8'))
                client.close()
                break

    def receive(self):
        while True:
            client, address = self.socket.accept()
            print(f'Connected with {str(address)}')

            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')

            if nickname in self.banned_users:
                client.send('BAN'.encode('utf-8'))
                client.close()
                continue

            if nickname in ADMINS:
                client.send('PASS'.encode('utf-8'))
                password = client.recv(1024).decode('utf-8')
                if hash(password) != ADMINS[nickname]:
                    client.send('REFUSE'.encode('utf-8'))
                    client.close()
                    continue

            self.clients[client] = nickname
            self.nicknames[nickname] = client

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
