import socket

#Criação do socket do server usando protocolo TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('0.0.0.0', 8080))

server_socket.listen(5)
print("Server waiting for connections...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} has been established!")

    with client_socket:
        try:
            message_received = client_socket.recv(1024)
            if not message_received:
                continue

            print(f"mesage from cliente: {message_received.decode('utf-8')}")

            client_socket.sendall(b"Welcome to the server! ")
        finally:
            client_socket.shutdown(socket.SHUT_RDWR)