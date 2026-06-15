import socket

#Criação o socket do cliente
client_socket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

# Pedir o IP do servidor ao usuário
server_ip = input("Digite o IP do servidor (padrão: 127.0.0.1): ") or "127.0.0.1"
porta = input("Digite a porta (padrão: 8080): ") or "8080"

try:
    client_socket.connect((server_ip, int(porta)))
    print("✓ Conectado ao servidor!")
    
    #Envio de mensagem para o servidor
    client_message = "Hi, server!"
    client_socket.sendall(client_message.encode('utf-8'))

    message = client_socket.recv(1024)
    print(f"Message from server: {message.decode('utf-8')}")
    
except ConnectionRefusedError:
    print("❌ Erro: Servidor não está disponível!")
except Exception as e:
    print(f"❌ Erro: {e}")
finally:
    try:
        client_socket.shutdown(socket.SHUT_RDWR)
    except:
        pass
    client_socket.close()
    print("✓ Conexão encerrada")
