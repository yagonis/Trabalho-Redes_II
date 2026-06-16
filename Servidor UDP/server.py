import socket

server_host = '0.0.0.0'
server_port = 8080
encerramento = ("sair", "/sair", "exit", "/exit", "quit", "/quit")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_host, server_port))

print(f"servidor UDP rodando em {server_host}:{server_port}")

while True:
    data, client_address = server_socket.recvfrom(1024)
    mensagem = data.decode('utf-8').strip()

    print(f"Mensagem recebida de {client_address}: {mensagem}")

    if mensagem.lower() in encerramento:
        resposta = "Conexão UDP encerrada com segurança."
        server_socket.sendto(resposta.encode('utf-8'), client_address)
        print(f"Conversa encerrada com {client_address}")
        continue

    resposta = "Olá, cliente UDP!"
    server_socket.sendto(resposta.encode('utf-8'), client_address)