# Chat WebSocket — Exercício 10
**Laboratório 31 | Prof. Alessandro Vivas Andrade**

---

## Estrutura do Projeto

```
chat_websocket/
├── servidor.py        ← Servidor WebSocket (rodar no PC servidor)
├── cliente.py         ← Cliente de terminal (rodar no PC cliente)
├── cliente_web.html   ← Cliente web (abrir no navegador)
└── README.md
```

---

## Pré-requisitos

```bash
pip3 install websockets
```

---

## Como Executar (dois computadores no Lab)

### PC 1 — Servidor

```bash
python3 servidor.py
# ou com porta personalizada:
python3 servidor.py 8765
```

Anote o IP da máquina:
```bash
hostname -I
```

### PC 2 — Cliente (terminal)

```bash
python3 cliente.py <IP_DO_SERVIDOR> 8765
```

### PC 2 — Cliente (navegador)

Abra `cliente_web.html` no navegador e preencha:
- **Servidor**: IP do PC 1
- **Porta**: 8765
- **Nome**: seu nome

---

## Protocolo WebSocket (JSON)

| Tipo               | Direção         | Campos                          |
|--------------------|-----------------|----------------------------------|
| `entrar`           | cliente → server| `tipo`, `nome`                  |
| `confirmacao`      | server → cliente| `tipo`, `texto`                 |
| `erro`             | server → cliente| `tipo`, `texto`                 |
| `mensagem`         | bidirecional    | `tipo`, `remetente`, `texto`, `hora` |
| `sistema`          | server → cliente| `tipo`, `texto`, `hora`         |
| `lista_usuarios`   | server → cliente| `tipo`, `usuarios[]`            |

---

## Funcionalidades

- ✅ Múltiplos clientes simultâneos
- ✅ Broadcast para todos ao enviar mensagem
- ✅ Notificação de entrada/saída de usuários
- ✅ Lista de usuários online em tempo real
- ✅ Validação de nomes duplicados
- ✅ Cliente terminal com cores ANSI
- ✅ Cliente web responsivo com interface gráfica
- ✅ Tratamento de desconexão inesperada

---

## Conceitos Demonstrados

1. **WebSocket** — protocolo full-duplex sobre TCP
2. **asyncio** — programação assíncrona em Python
3. **JSON** — serialização de mensagens no protocolo
4. **Broadcast** — envio de mensagem para N clientes
5. **Concorrência** — múltiplas conexões no servidor
