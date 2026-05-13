import socket

#Criação o socket do cliente
client_socket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('127.0.0.1', 8080))
try:
    #Envio de mensagem para o servidor
    client_message = "Hi, server!"
    client_socket.sendall(client_message.encode('utf-8'))

    message = client_socket.recv(1024)
    print(f"Message from server: {message.decode('utf-8')}")
finally:
    client_socket.close()
