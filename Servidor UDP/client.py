import socket

#Socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Pedir o IP do servidor ao usuário
server_ip = input("Digite o IP do servidor (padrão: 127.0.0.1): ") or "127.0.0.1"
porta = input("Digite a porta (padrão: 8080): ") or "8080"

#server address
server_address = (server_ip, int(porta))

try:
    #sent message to server
    message = "Hello, UDP Server!"
    client_socket.sendto(message.encode('utf-8'), server_address)
    print("✓ Mensagem enviada")

    #receive response from server
    data, server = client_socket.recvfrom(1024)
    print(f"Response from server: {data.decode('utf-8')}")
    
except Exception as e:
    print(f"❌ Erro: {e}")
finally:
    client_socket.close()
    print("✓ Socket fechado")