import socket

HOST = "127.0.0.1"
PORT = 7000

def solicitar_hora():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            cliente.connect((HOST, PORT))
            print(f"Conectado ao servidor {HOST}:{PORT}")

            # Envia a solicitação
            cliente.sendall("solicitar_hora".encode())

            # Recebe e exibe a hora
            hora = cliente.recv(1024).decode()
            print(f"Hora recebida do servidor: {hora}")

        except ConnectionRefusedError:
            print("Erro: não foi possível conectar ao servidor. Verifique se ele está rodando.")
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    solicitar_hora()