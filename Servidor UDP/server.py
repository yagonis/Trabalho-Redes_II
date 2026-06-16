import socket 

server_host = '0.0.0.0'
server_port = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_host, server_port))

print(f"servidor UDP rodando em {server_host}:{server_port}")

while True:
    data, client_address = server_socket.recvfrom(1024)
    print(f"Mensagem recebida de {client_address}: {data.decode('utf-8')}")

    resposta = "Olá, cliente UDP!"
    server_socket.sendto(resposta.encode('utf-8'), client_address)