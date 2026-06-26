# Simulador de Memória Virtual

Trabalho prático de Análise e Aplicação de Sistemas Operacionais.

Simula o gerenciamento de memória virtual com paginação: tradução de endereços pela MMU,
tratamento de page faults e substituição de páginas. Usa threads (processos leves) no
padrão produtor/consumidor.

## Vídeo

TODO

## Especificação

- Memória principal (RAM): 64 KB
- Memória virtual: 1 MB
- Página/frame: 8 KB
- Frames físicos: 8
- Páginas virtuais: 128
- Threads: 2
- Algoritmo de substituição: LRU (padrão) ou FIFO

## Como executar

Precisa só de Python 3.10+ (sem bibliotecas externas).

```bash
cd src
python main.py                  # LRU (padrão)
python main.py --algorithm fifo # FIFO
```

## Como funciona

Cada processo gera acessos à memória (página + offset). A MMU traduz esse endereço
virtual para o endereço físico (frame + offset):

- Se a página já está na RAM, lê o byte direto (hit).
- Se não está, ocorre um page fault: a página é carregada do disco para a RAM. Se não
  houver frame livre, o algoritmo de substituição (LRU ou FIFO) escolhe uma página para
  remover e abrir espaço.

As threads produtoras geram os acessos e colocam numa fila. A thread consumidora retira
da fila e chama a MMU. A MMU usa um lock para tratar um acesso por vez com segurança.

## Estrutura

```
src/
├── main.py            # ponto de entrada e escolha do algoritmo
├── config.py          # constantes do sistema
├── simulator.py       # monta e roda a simulação
├── models/            # estruturas de dados (acesso e resultado)
├── memory/            # disk.py, ram.py, page_table.py
├── replacement/       # base.py, lru.py, fifo.py
├── mmu/               # mmu.py (lógica de tradução e page fault)
└── threads/           # producer.py e consumer.py
```

As memórias (disk e ram) apenas guardam bytes. Toda a lógica fica na MMU. O algoritmo de
substituição é trocável sem alterar o resto do código.

## Exemplo de saída

```
[#001] Thread 0 | Page 8, Offset 2306
  >> PAGE FAULT
  >> Loaded into Frame 0
  >> Byte read: 205

[#009] Thread 0 | Page 22, Offset 1568
  >> PAGE FAULT
  >> Removed Page 8
  >> Loaded into Frame 0
  >> Byte read: 42

------------------------------------------------------------
  STATISTICS
------------------------------------------------------------
  Total accesses : 40
  Page hits      : 16
  Page faults    : 24
```
