import socket
import threading
import logging
from datetime import datetime

# Configuração do log
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%H:%M:%S"
)

HOST = "0.0.0.0"
PORT = 7000

def atender_cliente(conn, addr):
    """Função executada em thread separada para cada cliente."""
    try:
        logging.info(f"Cliente conectado: {addr}")

        # Recebe a solicitação do cliente
        dados = conn.recv(1024).decode()
        logging.info(f"Solicitação recebida de {addr}: '{dados}'")

        # Monta e envia a hora atual
        hora_atual = datetime.now().strftime("%H:%M:%S")
        conn.sendall(hora_atual.encode())

        logging.info(f"Hora enviada para {addr}: {hora_atual}")

    except Exception as e:
        logging.error(f"Erro ao atender {addr}: {e}")

    finally:
        conn.close()
        logging.info(f"Conexão encerrada: {addr}")

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen()

        logging.info(f"Servidor de hora rodando em {HOST}:{PORT}")
        logging.info("Aguardando conexões...")

        while True:
            try:
                conn, addr = servidor.accept()
                # Cria uma thread para cada cliente
                thread = threading.Thread(target=atender_cliente, args=(conn, addr))
                thread.daemon = True
                thread.start()
                logging.info(f"Threads ativas: {threading.active_count() - 1}")

            except Exception as e:
                logging.error(f"Erro no servidor: {e}")

if __name__ == "__main__":
    iniciar_servidor()