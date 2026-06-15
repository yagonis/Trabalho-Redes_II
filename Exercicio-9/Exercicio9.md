# Exercício 9 – Análise de Tráfego DHCP utilizando Wireshark

## Objetivo

Capturar e analisar o tráfego gerado pelo protocolo DHCP utilizando o software Wireshark, identificando o processo de concessão de endereço IP, os pacotes trocados e os endereços envolvidos.

---

## Procedimento

1. O Wireshark foi aberto e a captura de pacotes foi iniciada na interface `enp3s0`.
2. Foi executado o seguinte comando no terminal para forçar a renovação do endereço IP via DHCP:

```bash
sudo ip addr flush dev enp3s0 && sudo nmcli device connect enp3s0
```

3. A captura foi interrompida após a reconexão.
4. Foi aplicado o filtro `dhcp` para exibir apenas os pacotes do protocolo DHCP.

---

## Figura 1 – Captura DHCP no Wireshark

![Captura DHCP](image.png)

*Figura 1: Pacotes DHCP capturados durante a renovação de endereço IP na interface enp3s0.*

---

## Endereços Identificados

| Papel | Endereço IP |
|---|---|
| Cliente (antes da concessão) | `0.0.0.0` |
| Servidor DHCP (roteador) | `192.168.0.1` |
| Endereço de broadcast | `255.255.255.255` |

O cliente utiliza `0.0.0.0` como origem pois ainda não possui um endereço IP atribuído no momento da solicitação. As mensagens são enviadas para o endereço de broadcast `255.255.255.255` para alcançar todos os dispositivos na rede local.

---

## Pacotes Capturados

Foram capturados **2 pacotes DHCP**, correspondentes a um processo de renovação simplificado:

| Nº | Tempo (s) | Source | Destination | Tipo | Tamanho | Transaction ID |
|---|---|---|---|---|---|---|
| 6392 | 21.778 | `0.0.0.0` | `255.255.255.255` | DHCP Request | 324 bytes | `0x964bccac` |
| 6396 | 21.858 | `192.168.0.1` | `255.255.255.255` | DHCP ACK | 368 bytes | `0x964bccac` |

---

## Processo DHCP Observado

O processo capturado corresponde ao fluxo **Request → ACK**, que ocorre quando o cliente já possui um endereço IP anteriormente atribuído e tenta renová-lo diretamente com o servidor:

### DHCP Request (Pacote 6392)
- Enviado pelo cliente (`0.0.0.0`) via broadcast (`255.255.255.255`)
- O cliente solicita a renovação do endereço IP já conhecido
- Tamanho: **324 bytes**
- Transaction ID: `0x964bccac` — identificador único que vincula o Request ao ACK correspondente

### DHCP ACK (Pacote 6396)
- Enviado pelo servidor DHCP (`192.168.0.1`) via broadcast
- O servidor confirma a concessão do endereço IP ao cliente
- Tamanho: **368 bytes** (maior pois contém as opções DHCP com máscara, gateway, DNS, tempo de concessão)
- Mesmo Transaction ID `0x964bccac`, confirmando que é a resposta ao Request anterior

---

## Sobre o Processo DORA Completo

O protocolo DHCP define um processo completo de 4 etapas chamado **DORA**:

| Etapa | Mensagem | Quem envia | Descrição |
|---|---|---|---|
| 1 | **Discover** | Cliente → Broadcast | "Tem algum servidor DHCP na rede?" |
| 2 | **Offer** | Servidor → Cliente | "Sim! Te ofereço o IP 192.168.0.X" |
| 3 | **Request** | Cliente → Broadcast | "Quero esse IP que você ofereceu" |
| 4 | **ACK** | Servidor → Cliente | "Confirmado, o IP é seu!" |

Nesta captura, apenas as etapas **Request e ACK** foram observadas. Isso ocorreu porque o sistema operacional (Fedora com NetworkManager) identificou que o cliente já possuía um endereço IP anteriormente concedido e válido, otimizando o processo ao pular as etapas Discover e Offer, indo diretamente para a renovação. Esse comportamento é previsto pela **RFC 2131**, que especifica o protocolo DHCP.

---

## Latência da Concessão

| Evento | Timestamp |
|---|---|
| DHCP Request enviado | 21.778 s |
| DHCP ACK recebido | 21.858 s |
| **Tempo de resposta** | **~80 ms** |

O servidor DHCP respondeu em aproximadamente **80 milissegundos**, tempo baixo e esperado para uma rede local.

---

## Conclusão

A captura realizada no Wireshark permitiu observar o funcionamento do protocolo DHCP durante a renovação de endereço IP. Foram capturados 2 pacotes — um **DHCP Request** e um **DHCP ACK** — ambos vinculados pelo mesmo Transaction ID `0x964bccac`, confirmando que pertencem à mesma transação.

O processo observado foi uma renovação simplificada (Request → ACK), comportamento padrão do NetworkManager no Fedora quando o cliente já conhece um endereço IP anterior válido, conforme especificado pela RFC 2131. O servidor DHCP (`192.168.0.1`) respondeu em aproximadamente 80 ms, confirmando a concessão do endereço com sucesso.

Embora o fluxo DORA completo (Discover → Offer → Request → ACK) não tenha sido capturado nesta sessão, os pacotes obtidos demonstram as etapas finais e essenciais do protocolo, evidenciando a comunicação entre cliente e servidor DHCP e a concessão de endereçamento IP dinâmico na rede local.