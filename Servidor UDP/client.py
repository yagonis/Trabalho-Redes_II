import socket

server_host = input("Digite o IP do servidor (padrão: 127.0.0.1): ") or "127.0.0.1"
server_port = 8080
mensagens_saida = ("sair", "/sair", "exit", "/exit", "quit", "/quit")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
	while True:
		mensagem = input("Digite uma mensagem (ou 'sair' para encerrar): ")

		if not mensagem:
			continue

		client_socket.sendto(mensagem.encode('utf-8'), (server_host, server_port))

		data, server_address = client_socket.recvfrom(1024)
		resposta = data.decode('utf-8')
		print(f"Resposta do servidor: {resposta}")

		if mensagem.lower() in mensagens_saida or "encerrada" in resposta.lower():
			break
finally:
	client_socket.close()