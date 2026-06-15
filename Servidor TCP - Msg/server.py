import socket
import threading

# Lista para armazenar os clientes conectados
clientes = []
lock = threading.Lock()

def handle_cliente(cliente_socket, endereco, numero_cliente):
    """Função para gerenciar cada cliente conectado"""
    try:
        print(f"[Cliente {numero_cliente}] Conectado de {endereco}")
        
        while True:
            # Receber mensagem do cliente
            mensagem = cliente_socket.recv(1024).decode('utf-8')
            
            if not mensagem:
                break
            
            print(f"[Cliente {numero_cliente}] Mensagem: {mensagem}")
            
            # Transmitir a mensagem para o outro cliente
            with lock:
                for outro_cliente, outro_num in clientes:
                    if outro_cliente != cliente_socket:
                        try:
                            outro_cliente.sendall(f"[Cliente {numero_cliente}]: {mensagem}".encode('utf-8'))
                        except:
                            pass
    
    except Exception as e:
        print(f"[Cliente {numero_cliente}] Erro: {e}")
    
    finally:
        # Remover cliente da lista
        with lock:
            clientes[:] = [(c, n) for c, n in clientes if c != cliente_socket]
        
        try:
            cliente_socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        cliente_socket.close()
        print(f"[Cliente {numero_cliente}] Desconectado")
        
        # Notificar o outro cliente que este se desconectou
        with lock:
            for outro_cliente, outro_num in clientes:
                try:
                    outro_cliente.sendall(f"[Sistema] Cliente {numero_cliente} desconectou".encode('utf-8'))
                except:
                    pass

def main():
    # Criar socket do servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Vincular ao endereço e porta
    server_socket.bind(('0.0.0.0', 8080))
    
    # Começar a escutar conexões
    server_socket.listen(2)
    print("Servidor TCP aguardando conexões na porta 8080...")
    print("(Máximo de 2 clientes)\n")
    
    numero_cliente = 0
    
    try:
        while True:
            # Aceitar conexão de cliente
            cliente_socket, endereco = server_socket.accept()
            numero_cliente += 1
            
            # Verificar se já existem 2 clientes
            with lock:
                if len(clientes) >= 2:
                    cliente_socket.sendall(b"Servidor cheio! Apenas 2 clientes permitidos.")
                    cliente_socket.close()
                    print(f"Conexão rejeitada de {endereco} - Servidor cheio")
                    continue
                
                clientes.append((cliente_socket, numero_cliente))
            
            # Enviar mensagem de boas-vindas
            cliente_socket.sendall(f"Bem-vindo ao chat! Você é o Cliente {numero_cliente}\n".encode('utf-8'))
            
            # Se há 2 clientes, notificar que o chat pode começar
            with lock:
                if len(clientes) == 2:
                    for c, n in clientes:
                        try:
                            c.sendall(b"Segundo cliente conectado! Chat iniciado.\n")
                        except:
                            pass
            
            # Criar thread para gerenciar este cliente
            thread = threading.Thread(target=handle_cliente, args=(cliente_socket, endereco, numero_cliente))
            thread.daemon = True
            thread.start()
    
    except KeyboardInterrupt:
        print("\nServidor encerrando...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
