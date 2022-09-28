import socket
import threading

NICK = input('Choose a nickname: ')

HOST = '127.0.0.1'
PORT = 52525


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(NICK.encode('ascii'))
            else:
                print(message)
        except Exception as exc:
            print(f'An error occurred: {exc}')


def write():
    while True:
        message = f'{NICK}: {input("")}'
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)


if __name__ == '__main__':
    receive_thread.start()
    write_thread.start()


