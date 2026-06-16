import socket

server_host = input("Digite o IP do servidor (padrão: 127.0.0.1): ") or "127.0.0.1"
server_port = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mensagem = "Olá, servidor UDP!"

client_socket.sendto(mensagem.encode('utf-8'), (server_host, server_port))

data,server_address = client_socket.recvfrom(1024)
print(f"Resposta do servidor: {data.decode('utf-8')}")

client_socket.close()