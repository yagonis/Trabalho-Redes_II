#!/usr/bin/env python3
"""
==============================================================
 cliente.py — Cliente de Chat via WebSocket (Terminal)
==============================================================
 Disciplina : Redes de Computadores / Laboratório 31
 Professor  : Alessandro Vivas Andrade
 Exercício  : 10 — Chat com WebSockets
 Alunos     : 1. [SEU NOME AQUI]
              2. [NOME DO COLEGA]
              3. [NOME DO COLEGA]
==============================================================
 Descrição:
   Cliente de chat para terminal que se conecta ao servidor
   WebSocket. Utiliza uma thread dedicada para leitura do
   teclado (stdin) e asyncio para receber mensagens do
   servidor de forma concorrente, sem bloquear a interface.

 Como executar (Linux):
   python3 cliente.py [host] [porta]
   Exemplos:
     python3 cliente.py localhost 8765
     python3 cliente.py 192.168.1.10 8765

 Requisitos:
   pip3 install websockets
   Python >= 3.10
==============================================================
"""

import asyncio        # Event loop para operações assíncronas
import websockets     # Cliente WebSocket
import json           # Serialização de mensagens
import sys            # Argumentos e saída padrão
import threading      # Thread para leitura do teclado (stdin)


# --------------------------------------------------------------
# Funções auxiliares de terminal
# --------------------------------------------------------------

def limpar_linha() -> None:
    """
    Apaga a linha atual do terminal usando sequência de escape ANSI.
    Necessário para que mensagens recebidas não se misturem com
    o texto que o usuário está digitando.
    """
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()


def exibir_mensagem(dados: dict) -> None:
    """
    Formata e exibe no terminal uma mensagem recebida do servidor.
    Usa códigos de cor ANSI para diferenciar tipos de mensagem:
      - Ciano  (\033[1;36m): nome do remetente
      - Amarelo(\033[1;33m): mensagens de sistema (entrada/saída)
      - Verde  (\033[1;32m): confirmação de conexão
      - Vermelho(\033[1;31m): erros
      - Cinza  (\033[2m)   : lista de usuários online

    Args:
        dados (dict): Dicionário com os campos da mensagem.
    """
    tipo = dados.get("tipo")

    # Limpa a linha do prompt antes de imprimir
    limpar_linha()

    if tipo == "mensagem":
        # Mensagem de chat enviada por um usuário
        remetente = dados.get("remetente", "Desconhecido")
        texto = dados.get("texto", "")
        hora  = dados.get("hora", "")
        print(f"[{hora}] \033[1;36m{remetente}\033[0m: {texto}")

    elif tipo == "sistema":
        # Notificação do servidor (entrada/saída de usuários)
        texto = dados.get("texto", "")
        hora  = dados.get("hora", "")
        print(f"[{hora}] \033[1;33m*** {texto} ***\033[0m")

    elif tipo == "confirmacao":
        # Confirmação de conexão bem-sucedida
        print(f"\033[1;32m{dados.get('texto', '')}\033[0m")

    elif tipo == "erro":
        # Mensagem de erro enviada pelo servidor
        print(f"\033[1;31mERRO: {dados.get('texto', '')}\033[0m")

    elif tipo == "lista_usuarios":
        # Lista de usuários atualmente online
        usuarios = dados.get("usuarios", [])
        lista = ", ".join(usuarios) if usuarios else "nenhum"
        print(f"\033[2m[Usuários online: {lista}]\033[0m")

    # Reexibe o prompt de entrada após a mensagem
    sys.stdout.write("Você: ")
    sys.stdout.flush()


# --------------------------------------------------------------
# Corrotinas assíncronas
# --------------------------------------------------------------

async def receber_mensagens(websocket) -> None:
    """
    Corrotina que fica em loop aguardando mensagens do servidor
    e as exibe no terminal. Roda de forma concorrente com o
    envio de mensagens graças ao asyncio.

    Encerra automaticamente quando a conexão é fechada.

    Args:
        websocket: Objeto da conexão WebSocket ativa.
    """
    try:
        async for raw in websocket:
            dados = json.loads(raw)
            exibir_mensagem(dados)
    except websockets.exceptions.ConnectionClosed:
        # Servidor encerrou a conexão
        limpar_linha()
        print("\n\033[1;31m[Conexão com o servidor encerrada.]\033[0m")
    except json.JSONDecodeError as e:
        print(f"\n\033[1;31m[Erro ao decodificar mensagem: {e}]\033[0m")


async def enviar_mensagens(websocket, loop: asyncio.AbstractEventLoop) -> None:
    """
    Inicia uma thread separada para leitura do teclado (stdin),
    pois operações de input() bloqueiam o event loop do asyncio.
    A thread lê as linhas digitadas e as envia ao servidor via
    asyncio.run_coroutine_threadsafe(), que é a forma segura de
    submeter corrotinas a um event loop a partir de outra thread.

    Comandos especiais:
        /sair, /exit, /quit — encerra o cliente

    Args:
        websocket: Objeto da conexão WebSocket ativa.
        loop: Event loop do asyncio em execução.
    """

    def ler_teclado() -> None:
        """
        Função executada na thread auxiliar.
        Lê linhas do stdin e agenda o envio no event loop principal.
        """
        while True:
            try:
                # Exibe o prompt de entrada
                sys.stdout.write("Você: ")
                sys.stdout.flush()

                linha = sys.stdin.readline()

                # EOF (Ctrl+D no Linux) — encerra o cliente
                if not linha:
                    asyncio.run_coroutine_threadsafe(websocket.close(), loop)
                    break

                texto = linha.rstrip("\n").strip()

                # Comandos de saída
                if texto.lower() in ("/sair", "/exit", "/quit"):
                    asyncio.run_coroutine_threadsafe(websocket.close(), loop)
                    break

                # Ignora linhas vazias
                if not texto:
                    continue

                # Monta o payload JSON e agenda o envio no event loop
                payload = json.dumps(
                    {"tipo": "mensagem", "texto": texto},
                    ensure_ascii=False
                )
                asyncio.run_coroutine_threadsafe(
                    websocket.send(payload), loop
                )

            except (EOFError, KeyboardInterrupt):
                # Ctrl+C ou fim de entrada — encerra normalmente
                asyncio.run_coroutine_threadsafe(websocket.close(), loop)
                break

    # Inicia a thread de leitura como daemon (encerra com o programa)
    thread_teclado = threading.Thread(target=ler_teclado, daemon=True)
    thread_teclado.start()

    # Mantém a corrotina ativa enquanto a conexão WebSocket existir
    try:
        await websocket.wait_closed()
    except Exception:
        pass


async def conectar(host: str, porta: int) -> None:
    """
    Estabelece a conexão com o servidor WebSocket, realiza o
    handshake de entrada (enviando o nome do usuário) e inicia
    as corrotinas de envio e recebimento em paralelo.

    Args:
        host (str): Endereço IP ou hostname do servidor.
        porta (int): Porta TCP do servidor.
    """
    url = f"ws://{host}:{porta}"

    # Cabeçalho visual
    print("\033[1;34m╔══════════════════════════════════════╗")
    print("║     Chat WebSocket — Lab 31          ║")
    print("║     Prof. Alessandro Vivas Andrade   ║")
    print(f"╚══════════════════════════════════════╝\033[0m")
    print(f"Conectando a {url} ...\n")

    # Solicita o nome antes de conectar
    nome = ""
    while not nome.strip():
        nome = input("Seu nome: ").strip()
        if not nome:
            print("Nome não pode ser vazio. Tente novamente.")

    try:
        async with websockets.connect(url) as ws:
            # -------------------------------------------------
            # Handshake: envia o nome ao servidor
            # -------------------------------------------------
            await ws.send(json.dumps(
                {"tipo": "entrar", "nome": nome},
                ensure_ascii=False
            ))

            # Aguarda a resposta do servidor (confirmação ou erro)
            resposta_raw = await ws.recv()
            resposta = json.loads(resposta_raw)

            if resposta.get("tipo") == "erro":
                # Servidor rejeitou a conexão (ex: nome duplicado)
                print(f"\033[1;31mERRO: {resposta.get('texto')}\033[0m")
                return

            # Exibe a confirmação de boas-vindas
            exibir_mensagem(resposta)
            print("\033[2mDigite /sair para encerrar o chat.\033[0m\n")

            # Obtém o event loop atual para passar à thread de leitura
            loop = asyncio.get_event_loop()

            # Executa recebimento e envio de mensagens em paralelo
            # usando asyncio.gather() — equivalente a duas "threads" assíncronas
            await asyncio.gather(
                receber_mensagens(ws),
                enviar_mensagens(ws, loop)
            )

    except ConnectionRefusedError:
        # Servidor não está acessível no endereço/porta informados
        print(f"\033[1;31mNão foi possível conectar a {url}.")
        print("Verifique se o servidor está rodando e o IP/porta estão corretos.\033[0m")

    except OSError as e:
        # Erro de rede genérico (ex: host inválido)
        print(f"\033[1;31mErro de rede: {e}\033[0m")

    except Exception as e:
        # Captura qualquer outro erro inesperado
        print(f"\033[1;31mErro inesperado: {e}\033[0m")

    print("\n[Chat encerrado]")


# --------------------------------------------------------------
# Ponto de entrada principal
# --------------------------------------------------------------
if __name__ == "__main__":
    # Lê host e porta opcionais da linha de comando
    host  = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    porta = 8765
    if len(sys.argv) > 2:
        try:
            porta = int(sys.argv[2])
        except ValueError:
            print("Porta inválida. Usando 8765.")

    try:
        asyncio.run(conectar(host, porta))
    except KeyboardInterrupt:
        print("\n[Saindo...]")
