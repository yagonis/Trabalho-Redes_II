import socket

#Socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('127.0.0.1', 8080)
server_socket.bind(server_address)

print("UDP Server is up and listening...")

try:
    while True:
        try:
            data, client_address = server_socket.recvfrom(1024)
            print(f"Received message from {client_address}: {data.decode('utf-8')}")

            response = "Message received with success!"
            server_socket.sendto(response.encode('utf-8'), client_address)
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
except KeyboardInterrupt:
    print("\n✓ Servidor encerrando...")
finally:
    server_socket.close()
    print("✓ Socket do servidor fechado")