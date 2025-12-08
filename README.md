# 📱 Agenda Telefônica Dinâmica (AVL Tree)

Este repositório contém o Trabalho Prático da disciplina de **Algoritmos e Estruturas de Dados II**, ministrada pelo Prof. Alternei Brito na Universidade Federal do Amazonas (UFAM).

O projeto consiste na implementação de uma **Agenda Telefônica** utilizando uma **Árvore AVL** (Árvore Binária de Busca Balanceada) para garantir alta performance nas operações de busca, inserção e remoção ($O(\log n)$).

## 👥 Equipe
* Gustavo Pinheiro de Souza
* Jean Carlos dos Santos Baraúna
* Kaio Sobral Moreira
* Luan Batalha Pinto
* Ricky Brendon da Silva Almeida

## 🚀 Funcionalidades
* **Estrutura de Dados:** Implementação pura de Árvore AVL (sem bibliotecas externas de árvores).
* **Balanceamento Automático:** Rotações simples e duplas para manter a árvore equilibrada.
* **Persistência de Dados:** Salva e carrega contatos automaticamente em arquivo de texto.
* **Interface Gráfica (GUI):** Interface amigável desenvolvida com `tkinter` para visualização das estatísticas da árvore (altura, rotações).
* **Busca e Edição:** Permite buscar contatos exatos e editar informações mantendo a integridade da árvore.

## 📂 Estrutura de Arquivos

* `Agenda Telefonica Dinamica.py`: Código fonte principal contendo a classe `AVLTree`, `Node` e a interface gráfica.
* `agenda.txt`: Arquivo de banco de dados onde os contatos são salvos automaticamente (formato `Nome|Telefone`).

## 🛠️ Como Executar

### Pré-requisitos
* Python 3.x instalado.
* Biblioteca `tkinter` (geralmente já vem instalada com o Python).
