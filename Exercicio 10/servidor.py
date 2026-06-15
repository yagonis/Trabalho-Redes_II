#!/usr/bin/env python3
"""
==============================================================
 servidor.py — Servidor de Chat via WebSocket
==============================================================
 Disciplina : Redes de Computadores / Laboratório 31
 Professor  : Alessandro Vivas Andrade
 Exercício  : 10 — Chat com WebSockets
 Alunos     : 1. [SEU NOME AQUI]
              2. [NOME DO COLEGA]
              3. [NOME DO COLEGA]
==============================================================
 Descrição:
   Servidor assíncrono (asyncio + websockets) que aceita
   múltiplas conexões simultâneas de clientes via protocolo
   WebSocket. Cada mensagem recebida é retransmitida (broadcast)
   para todos os clientes conectados. Utiliza threads implícitas
   via event loop do asyncio para concorrência.

 Como executar (Linux):
   python3 servidor.py [porta]
   Exemplo: python3 servidor.py 8765

 Requisitos:
   pip3 install websockets
   Python >= 3.10
==============================================================
"""

import asyncio        # Gerenciamento de I/O assíncrono (event loop)
import websockets     # Biblioteca WebSocket para Python
import json           # Serialização/deserialização de mensagens
import sys            # Argumentos de linha de comando
from datetime import datetime  # Registro de horário nas mensagens

# --------------------------------------------------------------
# Estado global do servidor
# Dicionário que mapeia cada conexão WebSocket ao nome do usuário
# Estrutura: { websocket_objeto: "nome_do_usuario" }
# --------------------------------------------------------------
clientes = {}


def log(mensagem: str) -> None:
    """
    Exibe uma mensagem de log no terminal do servidor
    com o horário atual no formato [HH:MM:SS].

    Args:
        mensagem (str): Texto a ser exibido no log.
    """
    hora = datetime.now().strftime("%H:%M:%S")
    print(f"[{hora}] {mensagem}")


async def broadcast(mensagem_dict: dict, excluir=None) -> None:
    """
    Envia uma mensagem (em formato JSON) para TODOS os clientes
    conectados, com opção de excluir um cliente específico.

    Implementa o padrão de broadcast: o servidor retransmite
    a mensagem de um remetente para todos os demais.

    Args:
        mensagem_dict (dict): Dicionário com os dados da mensagem.
        excluir: Conexão WebSocket a ser ignorada no envio (opcional).
    """
    if not clientes:
        return  # Nenhum cliente conectado, nada a fazer

    # Serializa o dicionário para string JSON
    mensagem_json = json.dumps(mensagem_dict, ensure_ascii=False)

    # Copia a lista para evitar erros caso o dict mude durante iteração
    destinatarios = list(clientes.keys())

    for ws in destinatarios:
        if ws == excluir:
            continue  # Pula o cliente excluído (ex: não ecoar para o remetente)
        try:
            await ws.send(mensagem_json)
        except websockets.exceptions.ConnectionClosed:
            # Cliente desconectou antes de receber — ignora silenciosamente
            pass


async def atualizar_lista_usuarios() -> None:
    """
    Envia para todos os clientes a lista atualizada de
    usuários conectados no momento. Útil para manter a
    barra lateral do cliente web sincronizada.
    """
    nomes = list(clientes.values())
    await broadcast({
        "tipo": "lista_usuarios",
        "usuarios": nomes
    })


async def handler(websocket) -> None:
    """
    Corrotina principal que gerencia o ciclo de vida de cada
    cliente conectado. É chamada automaticamente pelo servidor
    WebSocket a cada nova conexão — o asyncio executa múltiplas
    instâncias desta função de forma concorrente (sem threads do SO).

    Fluxo:
        1. Recebe e valida o nome do usuário
        2. Registra o cliente e notifica os demais
        3. Loop: aguarda e retransmite mensagens (broadcast)
        4. Ao desconectar: remove o cliente e notifica os demais

    Args:
        websocket: Objeto da conexão WebSocket do cliente.
    """
    nome = None  # Nome do usuário (definido após autenticação)

    try:
        # ----------------------------------------------------------
        # ETAPA 1: Handshake — receber o nome do usuário
        # O primeiro pacote deve ser do tipo "entrar"
        # ----------------------------------------------------------
        dados_raw = await websocket.recv()
        dados = json.loads(dados_raw)

        # Validação do tipo de mensagem esperada
        if dados.get("tipo") != "entrar":
            await websocket.send(json.dumps({
                "tipo": "erro",
                "texto": "Protocolo inválido. Esperado tipo 'entrar'."
            }))
            return

        # Validação do nome: não pode ser vazio
        nome = dados.get("nome", "").strip()
        if not nome:
            await websocket.send(json.dumps({
                "tipo": "erro",
                "texto": "Nome inválido. Informe um nome não vazio."
            }))
            return

        # Validação: nome não pode estar em uso por outro cliente
        if nome in clientes.values():
            await websocket.send(json.dumps({
                "tipo": "erro",
                "texto": f"Nome '{nome}' já está em uso. Escolha outro."
            }))
            return

        # Registra o cliente no dicionário global
        clientes[websocket] = nome
        log(f"ENTRADA  '{nome}' conectou. ({len(clientes)} online)")

        # Confirma a entrada ao próprio cliente
        await websocket.send(json.dumps({
            "tipo": "confirmacao",
            "texto": f"Bem-vindo, {nome}! Você está conectado ao chat."
        }))

        # Notifica todos os outros clientes sobre o novo usuário
        await broadcast({
            "tipo": "sistema",
            "texto": f"{nome} entrou no chat.",
            "hora": datetime.now().strftime("%H:%M")
        }, excluir=websocket)

        # Atualiza a lista de usuários em todos os clientes
        await atualizar_lista_usuarios()

        # ----------------------------------------------------------
        # ETAPA 2: Loop de mensagens
        # Aguarda mensagens do cliente e faz broadcast para todos
        # ----------------------------------------------------------
        async for mensagem_raw in websocket:
            try:
                dados = json.loads(mensagem_raw)
            except json.JSONDecodeError:
                # Mensagem malformada — ignora e continua
                log(f"AVISO    Mensagem inválida de '{nome}' ignorada.")
                continue

            if dados.get("tipo") == "mensagem":
                texto = dados.get("texto", "").strip()

                # Validação: mensagem não pode ser vazia
                if not texto:
                    continue

                # Limita o tamanho da mensagem a 500 caracteres
                if len(texto) > 500:
                    texto = texto[:500] + "..."

                hora = datetime.now().strftime("%H:%M")
                log(f"MENSAGEM '{nome}': {texto}")

                # Retransmite a mensagem para todos os clientes (broadcast)
                await broadcast({
                    "tipo": "mensagem",
                    "remetente": nome,
                    "texto": texto,
                    "hora": hora
                })

    except websockets.exceptions.ConnectionClosed:
        # Desconexão normal — encerra silenciosamente o handler
        pass

    except json.JSONDecodeError as e:
        # Erro ao decodificar JSON no pacote inicial
        log(f"ERRO     JSON inválido no handshake: {e}")

    except Exception as e:
        # Captura erros inesperados para não derrubar o servidor
        log(f"ERRO     Exceção inesperada com '{nome}': {e}")

    finally:
        # ----------------------------------------------------------
        # ETAPA 3: Limpeza ao desconectar
        # Sempre executado, mesmo em caso de erro
        # ----------------------------------------------------------
        if websocket in clientes:
            del clientes[websocket]  # Remove o cliente do registro global

        if nome:
            log(f"SAIDA    '{nome}' desconectou. ({len(clientes)} online)")
            # Notifica os demais sobre a saída
            await broadcast({
                "tipo": "sistema",
                "texto": f"{nome} saiu do chat.",
                "hora": datetime.now().strftime("%H:%M")
            })
            # Atualiza a lista de usuários
            await atualizar_lista_usuarios()


async def iniciar_servidor(host: str = "0.0.0.0", porta: int = 8765) -> None:
    """
    Inicializa o servidor WebSocket e mantém em execução
    indefinidamente até ser interrompido (Ctrl+C).

    O host "0.0.0.0" significa que o servidor aceita conexões
    de qualquer interface de rede (local e rede interna).

    Args:
        host (str): Endereço de escuta (padrão: todas as interfaces).
        porta (int): Porta TCP de escuta (padrão: 8765).
    """
    log(f"Servidor WebSocket iniciado em ws://{host}:{porta}")
    log("Aguardando conexões... (Ctrl+C para encerrar)\n")

    # websockets.serve() cria o servidor e chama handler() para
    # cada nova conexão — o asyncio gerencia a concorrência
    async with websockets.serve(handler, host, porta):
        await asyncio.Future()  # Bloqueia indefinidamente (event loop ativo)


# --------------------------------------------------------------
# Ponto de entrada principal
# --------------------------------------------------------------
if __name__ == "__main__":
    # Permite definir a porta via argumento: python3 servidor.py 9000
    porta = 8765
    if len(sys.argv) > 1:
        try:
            porta = int(sys.argv[1])
            if not (1 <= porta <= 65535):
                raise ValueError("Porta fora do intervalo válido (1-65535).")
        except ValueError as e:
            print(f"Porta inválida: {e}. Usando porta padrão 8765.")
            porta = 8765

    try:
        asyncio.run(iniciar_servidor(porta=porta))
    except KeyboardInterrupt:
        print("\n\n[Servidor encerrado pelo usuário]")
