import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # ✅ Fix

porta = int(input("Porta (padrão 8080): ") or "8080")  # ✅ Configurável
server_socket.bind(('0.0.0.0', porta))
print(f"Servidor UDP ouvindo na porta {porta}...")

try:
    while True:
        try:
            data, client_address = server_socket.recvfrom(1024)
            mensagem = data.decode('utf-8', errors='replace')  # ✅ Não quebra
            print(f"Recebido de {client_address}: {mensagem}")
            server_socket.sendto("Mensagem recebida!".encode('utf-8'), client_address)
        except UnicodeDecodeError as e:
            print(f"Erro de encoding: {e}")  # ✅ Erro específico
        except OSError as e:
            print(f"Erro de socket crítico: {e}")
            break  # ✅ Para o loop em erros graves
except KeyboardInterrupt:
    print("\n✓ Servidor encerrando...")
finally:
    server_socket.close()