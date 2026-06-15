import socket
import threading

HOST = "127.0.0.1"
PORT = 7000

def cliente_simulado(id_cliente):
    """Função que simula um único cliente."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            cliente.connect((HOST, PORT))
            cliente.sendall("solicitar_hora".encode())
            hora = cliente.recv(1024).decode()
            print(f"[Cliente {id_cliente}] Recebeu a hora: {hora}")
        except Exception as e:
            print(f"[Cliente {id_cliente}] Falhou: {e}")

# Criando 10 clientes simultâneos
threads_clientes = []
print("Iniciando ataque de clientes simultâneos...")

for i in range(1, 11):
    # Cria uma thread para cada cliente
    t = threading.Thread(target=cliente_simulado, args=(i,))
    threads_clientes.append(t)
    t.start()

# Aguarda todos os clientes terminarem
for t in threads_clientes:
    t.join()

print("Teste de carga finalizado.")