import errno
import socket
import threading

from sys import argv

HOST = argv[1]
PORT = int(argv[2])
HEADER_LENGTH = 10


def receive_message(client_socket):
    while True:
        try:
            username_header = client_socket.recv(HEADER_LENGTH)

            if not len(username_header):
                print("Connection lost")
                exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f"{username} > {message}")

        except IOError as error:
            if error.errno != errno.EAGAIN and error.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(error)))
                exit()

            continue

        except Exception as error:
            # Any other exception - something happened, exit
            print('Reading error: '.format(str(error)))
            exit()


if __name__ == '__main__':
    my_username = input("Username: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.setblocking(False)

    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)

    thread = threading.Thread(target=receive_message, args=(client_socket,)).start()

    while True:
        try:
            message = input(f"{my_username} > ")

            if message:
                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + message)

        except IOError as error:
            if error.errno != errno.EAGAIN and error.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(error)))
                exit()

            continue

        except Exception as error:
            # Any other exception - something happened, exit
            print('Reading error: '.format(str(error)))
            exit()
