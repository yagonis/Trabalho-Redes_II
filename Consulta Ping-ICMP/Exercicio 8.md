# Exercício 8 – Análise de Tráfego ICMP com o Comando Ping utilizando Wireshark
## Alunos - Ian Patrick, Maria Vieira, Miguel Moreira, Yago Brito

## Objetivo

Capturar e analisar o tráfego gerado pelo comando `ping` utilizando o software Wireshark, identificando os pacotes ICMP trocados entre os hosts, os campos relevantes do protocolo e o comportamento da comunicação.

---

## Procedimento

1. O Wireshark foi aberto e a captura de pacotes foi iniciada na interface de rede cabeada (`enp3s0`).
2. Foi executado o comando abaixo no terminal:

```bash
ping -c 4 192.168.0.1
```

3. A captura foi interrompida após a conclusão do comando.
4. Foi aplicado o filtro `icmp` para exibir apenas os pacotes do protocolo ICMP.

---

## Figura 1 – Captura ICMP no Wireshark

![Captura ICMP](image.png)

*Figura 1: Pacotes ICMP capturados durante a execução do comando ping para 192.168.0.1.*

---

## Endereços Identificados

| Papel | Endereço IP |
|---|---|
| Cliente (máquina local) | `192.168.0.179` |
| Destino (gateway/roteador) | `192.168.0.1` |

Ambos os hosts pertencem à mesma rede local (`192.168.0.0/24`), portanto a comunicação ocorre diretamente, sem passar por roteadores intermediários.

---

## Pacotes Capturados

Foram capturados **8 pacotes ICMP** — resultado de 4 pings, cada um gerando 1 Echo Request e 1 Echo Reply:

| Nº | Tempo (s) | Source | Destination | Tipo | Sequência | TTL |
|---|---|---|---|---|---|---|
| 543 | 10.542053 | 192.168.0.179 | 192.168.0.1 | Echo Request | 1/256 | 64 |
| 544 | 10.542560 | 192.168.0.1 | 192.168.0.179 | Echo Reply | 1/256 | 64 |
| 545 | 11.604049 | 192.168.0.179 | 192.168.0.1 | Echo Request | 2/512 | 64 |
| 546 | 11.604589 | 192.168.0.1 | 192.168.0.179 | Echo Reply | 2/512 | 64 |
| 547 | 12.628042 | 192.168.0.179 | 192.168.0.1 | Echo Request | 3/768 | 64 |
| 548 | 12.628559 | 192.168.0.1 | 192.168.0.179 | Echo Reply | 3/768 | 64 |
| 549 | 13.652019 | 192.168.0.179 | 192.168.0.1 | Echo Request | 4/1024 | 64 |
| 550 | 13.652544 | 192.168.0.1 | 192.168.0.179 | Echo Reply | 4/1024 | 64 |

---

## Análise dos Campos ICMP

### Tipo de Mensagem

O protocolo ICMP utiliza o campo **Type** para identificar o tipo de mensagem:

| Tipo ICMP | Valor | Descrição |
|---|---|---|
| Echo Request | Type 8 | Enviado pelo cliente para testar conectividade |
| Echo Reply | Type 0 | Resposta enviada pelo destino confirmando recebimento |

### Identificador (ID)

Todos os pacotes compartilham o mesmo identificador `0x5ecb`, o que os agrupa como pertencentes à mesma sessão de ping.

### Número de Sequência

Os números de sequência sobem progressivamente de **256 em 256** (256, 512, 768, 1024), permitindo identificar e ordenar cada par request/reply e detectar possíveis perdas de pacotes.

### Tamanho dos Pacotes

Todos os pacotes têm **98 bytes**, valor padrão do comando `ping` no Linux (20 bytes IP + 8 bytes ICMP + 70 bytes de payload).

### TTL (Time to Live)

O TTL de **64** é o valor padrão do Linux. Como o destino está na mesma rede local e respondeu com TTL 64, confirma-se que a comunicação ocorreu **sem passar por nenhum roteador intermediário** — o pacote chegou diretamente.

---

## Análise de Latência

Comparando o timestamp do Echo Request com o Echo Reply de cada par:

| Ping | Request (s) | Reply (s) | Latência aproximada |
|---|---|---|---|
| 1 | 10.542053 | 10.542560 | ~0,5 ms |
| 2 | 11.604049 | 11.604589 | ~0,5 ms |
| 3 | 12.628042 | 12.628559 | ~0,5 ms |
| 4 | 13.652019 | 13.652544 | ~0,5 ms |

A latência constante de aproximadamente **0,5 ms** indica uma conexão local estável e sem congestionamento.

---

## Intervalo Entre Pings

O comando `ping` no Linux envia um pacote a cada **1 segundo** por padrão:

| De | Para | Intervalo |
|---|---|---|
| Ping 1 → Ping 2 | 10.542 → 11.604 | ~1,06 s |
| Ping 2 → Ping 3 | 11.604 → 12.628 | ~1,02 s |
| Ping 3 → Ping 4 | 12.628 → 13.652 | ~1,02 s |

---

## Processo de Comunicação ICMP

1. O comando `ping -c 4 192.168.0.1` foi executado no terminal.
2. O sistema operacional criou 4 pacotes **ICMP Echo Request** (Type 8), numerados sequencialmente.
3. Cada pacote foi enviado do cliente (`192.168.0.179`) ao destino (`192.168.0.1`) com intervalo de ~1 segundo.
4. O roteador de destino recebeu cada Request e respondeu imediatamente com um **ICMP Echo Reply** (Type 0).
5. O cliente recebeu as 4 respostas, confirmando conectividade completa com o host de destino.
6. Nenhum pacote foi perdido — todos os 4 Requests obtiveram Reply correspondente.

---

## Conclusão

A captura realizada no Wireshark permitiu observar na prática o funcionamento do protocolo **ICMP** durante a execução do comando `ping`. Foram capturados 8 pacotes (4 Echo Requests e 4 Echo Replies), todos com 98 bytes e TTL igual a 64.

A análise demonstrou que a comunicação entre o cliente (`192.168.0.179`) e o gateway (`192.168.0.1`) ocorreu de forma direta, sem roteadores intermediários, com latência média de aproximadamente **0,5 ms**, indicando uma rede local estável e eficiente.

O uso do número de sequência no protocolo ICMP permitiu identificar e correlacionar cada par de Request/Reply, evidenciando que **nenhum pacote foi perdido** durante o teste — taxa de entrega de 100%.