import socket
import threading
import sys

class ClienteChat:
    def __init__(self, host=None, porta=None):
        # Se não fornecido, pedir ao usuário
        if host is None:
            self.host = input("Digite o IP do servidor (padrão: 127.0.0.1): ") or "127.0.0.1"
        else:
            self.host = host
        
        if porta is None:
            porta_input = input("Digite a porta (padrão: 8080): ") or "8080"
            self.porta = int(porta_input)
        else:
            self.porta = porta
        self.socket = None
        self.conectado = False
    
    def conectar(self):
        """Conectar ao servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.porta))
            self.conectado = True
            print("Conectado ao servidor!")
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            self.conectado = False
            return False
        return True
    
    def receber_mensagens(self):
        """Thread para receber mensagens do servidor"""
        while self.conectado:
            try:
                mensagem = self.socket.recv(1024).decode('utf-8')
                
                if not mensagem:
                    break
                
                print(f"\n{mensagem}")
                print("Você: ", end="", flush=True)
            
            except:
                break
        
        self.conectado = False
    
    def enviar_mensagens(self):
        """Thread para enviar mensagens para o servidor"""
        while self.conectado:
            try:
                mensagem = input("Você: ")
                
                if mensagem.lower() == "sair":
                    print("Encerrando chat...")
                    self.conectado = False
                    self.socket.close()
                    break
                
                if mensagem:
                    self.socket.sendall(mensagem.encode('utf-8'))
            
            except:
                break
        
        self.conectado = False
    
    def iniciar_chat(self):
        """Iniciar o chat com threads para envio e recebimento"""
        if not self.conectar():
            return
        
        # Thread para receber mensagens
        thread_receber = threading.Thread(target=self.receber_mensagens)
        thread_receber.daemon = True
        thread_receber.start()
        
        # Thread para enviar mensagens
        thread_enviar = threading.Thread(target=self.enviar_mensagens)
        thread_enviar.daemon = True
        thread_enviar.start()
        
        # Esperar as threads terminarem
        thread_receber.join()
        thread_enviar.join()
        
        print("Desconectado do servidor.")

def main():
    cliente = ClienteChat()
    cliente.iniciar_chat()

if __name__ == "__main__":
    main()
