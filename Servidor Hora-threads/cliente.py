import socket

def solicitar_hora():
    host = input("Digite o IP do servidor: ")
    porta = input("Digite a porta do servidor: ")

    try:
        porta = int(porta)
    except ValueError:
        print("Erro: a porta deve ser um número.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            cliente.connect((host, porta))
            print(f"Conectado ao servidor {host}:{porta}")

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