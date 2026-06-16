# Trabalho - Redes II 🌐

[![Python](https://img.shields.io/badge/Python-69%25-blue)](#linguagens-utilizadas)
[![HTML](https://img.shields.io/badge/HTML-31%25-orange)](#linguagens-utilizadas)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#licença)

Repositório contendo implementações de servidores e ferramentas de rede para a disciplina de **Redes II**.

## 📋 Sobre

Este projeto é um trabalho acadêmico que implementa diversos servidores de comunicação em rede utilizando **Python**, com foco em protocolos TCP/UDP, análise de tráfego de rede e conceitos fundamentais de redes de computadores.

## 📂 Estrutura do Projeto

```
Trabalho-Redes_II/
├── Servidor TCP/                    # Implementação básica de servidor TCP
├── Servidor TCP - Msg/              # Servidor TCP com troca de mensagens
├── Servidor UDP/                    # Implementação de servidor UDP
├── Servidor Hora-threads/           # Servidor de hora com suporte a threads
├── Exercicio 5/                     # Exercício 5 da disciplina
├── Exercicio 6/                     # Exercício 6 da disciplina
├── Exercicio 10/                    # Exercício 10 da disciplina
├── Exercicio-9/                     # Exercício 9 da disciplina
├── Consulta Ping-ICMP/              # Análise de consultas PING (ICMP)
├── Consulta DNS- WireShark/         # Análise de consultas DNS com WireShark
└── README.md                         # Este arquivo
```

## 🛠️ Componentes Principais

### Servidores de Rede

#### **Servidor TCP**
Implementação básica de um servidor TCP que aceita conexões de clientes.

#### **Servidor TCP - Msg**
Servidor TCP com funcionalidade de troca de mensagens entre cliente e servidor.

#### **Servidor UDP**
Implementação de um servidor baseado no protocolo UDP (User Datagram Protocol).

#### **Servidor Hora - Threads**
Servidor que fornece a hora atual e utiliza threads para atender múltiplos clientes simultaneamente.

### Exercícios Práticos

- **Exercício 5, 6, 9, 10**: Tarefas práticas da disciplina que implementam conceitos diversos de rede

### Análise de Protocolo

- **Consulta Ping-ICMP**: Análise de requisições ICMP (Internet Control Message Protocol)
- **Consulta DNS-WireShark**: Análise de tráfego DNS utilizando a ferramenta WireShark

## 💻 Linguagens Utilizadas

- **Python** (69%) - Implementação dos servidores e ferramentas
- **HTML** (31%) - Documentação e interfaces web

## 🚀 Como Usar

### Pré-requisitos

- Python 3.x instalado
- Conhecimento básico de protocolos de rede (TCP/UDP)

### Executando um Servidor

```bash
# Exemplo: Executar o Servidor TCP
cd "Servidor TCP"
python servidor.py

# Exemplo: Executar o Servidor UDP
cd "Servidor UDP"
python servidor.py
```

### Conectando a um Servidor

```bash
# Usando telnet (TCP)
telnet localhost 5000

# Usando netcat (UDP)
nc -u localhost 5000
```

## 📝 Tópicos Cobertos

- ✅ Protocolos TCP e UDP
- ✅ Sockets em Python
- ✅ Multi-threading em servidores
- ✅ Protocolo ICMP (Ping)
- ✅ Protocolo DNS
- ✅ Análise de tráfego com WireShark
- ✅ Programação cliente-servidor

## 🎓 Disciplina

**Redes II** - Trabalho Acadêmico

## 📄 Licença

Este projeto é fornecido como material educacional para a disciplina de Redes II.

## 👤 Autor

**yagonis** - [GitHub Profile](https://github.com/yagonis)

---

**Última atualização:** junho de 2026

> 💡 **Dica:** Explore cada diretório para encontrar exemplos específicos e testes de funcionamento dos servidores e ferramentas implementadas.
