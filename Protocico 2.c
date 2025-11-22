/*
 * ====================================================================
 * AGENDA TELEFÔNICA COM ÁRVORE AVL
 * Trabalho Prático - Algoritmos e Estruturas de Dados II
 * ====================================================================
 * Implementação de uma agenda telefônica utilizando Árvore AVL
 * (Adelson-Velsky and Landis) para armazenamento balanceado.
 * ====================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Definições de constantes
#define MAX_NOME 100
#define MAX_TELEFONE 20
#define MAX_EMAIL 100
#define ARQUIVO_DADOS "agenda.txt"

// ====================================================================
// ESTRUTURAS DE DADOS
// ====================================================================

/**
 * Estrutura que representa um contato individual
 * Armazena nome, telefone e email
 */
typedef struct {
    char nome[MAX_NOME];
    char telefone[MAX_TELEFONE];
    char email[MAX_EMAIL];
} Contato;

/**
 * Estrutura de um nó da Árvore AVL
 * Contém o contato, ponteiros para filhos e altura do nó
 */
typedef struct No {
    Contato contato;
    struct No *esquerda;  // Subárvore esquerda (contatos com nomes menores)
    struct No *direita;   // Subárvore direita (contatos com nomes maiores)
    int altura;           // Altura do nó (usado para balanceamento)
} No;

// ====================================================================
// FUNÇÕES AUXILIARES DA ÁRVORE AVL
// ====================================================================

/**
 * Retorna o maior valor entre dois inteiros
 */
int max(int a, int b) {
    return (a > b) ? a : b;
}

/**
 * Retorna a altura de um nó
 * Se o nó for NULL, retorna 0
 */
int altura(No *no) {
    if (no == NULL)
        return 0;
    return no->altura;
}

/**
 * Calcula o fator de balanceamento de um nó
 * FB = altura(subárvore esquerda) - altura(subárvore direita)
 * FB > 1: árvore desbalanceada para esquerda
 * FB < -1: árvore desbalanceada para direita
 */
int fatorBalanceamento(No *no) {
    if (no == NULL)
        return 0;
    return altura(no->esquerda) - altura(no->direita);
}

/**
 * Atualiza a altura de um nó baseada nas alturas dos filhos
 */
void atualizarAltura(No *no) {
    if (no != NULL) {
        no->altura = 1 + max(altura(no->esquerda), altura(no->direita));
    }
}

// ====================================================================
// ROTAÇÕES DA ÁRVORE AVL
// ====================================================================

/**
 * Rotação Simples à Direita (LL)
 * Usada quando há desbalanceamento à esquerda-esquerda
 * 
 *       y                    x
 *      / \                  / \
 *     x   C   ----->       A   y
 *    / \                      / \
 *   A   B                    B   C
 */
No* rotacaoDireita(No *y) {
    No *x = y->esquerda;
    No *B = x->direita;

    // Executa a rotação
    x->direita = y;
    y->esquerda = B;

    // Atualiza as alturas (primeiro o filho, depois o pai)
    atualizarAltura(y);
    atualizarAltura(x);

    return x; // Nova raiz da subárvore
}

/**
 * Rotação Simples à Esquerda (RR)
 * Usada quando há desbalanceamento à direita-direita
 * 
 *     x                      y
 *    / \                    / \
 *   A   y     ----->       x   C
 *      / \                / \
 *     B   C              A   B
 */
No* rotacaoEsquerda(No *x) {
    No *y = x->direita;
    No *B = y->esquerda;

    // Executa a rotação
    y->esquerda = x;
    x->direita = B;

    // Atualiza as alturas (primeiro o filho, depois o pai)
    atualizarAltura(x);
    atualizarAltura(y);

    return y; // Nova raiz da subárvore
}

/**
 * Rotação Dupla à Direita (LR)
 * Usada quando há desbalanceamento à esquerda-direita
 * Combina: rotação esquerda no filho esquerdo + rotação direita na raiz
 */
No* rotacaoEsquerdaDireita(No *no) {
    no->esquerda = rotacaoEsquerda(no->esquerda);
    return rotacaoDireita(no);
}

/**
 * Rotação Dupla à Esquerda (RL)
 * Usada quando há desbalanceamento à direita-esquerda
 * Combina: rotação direita no filho direito + rotação esquerda na raiz
 */
No* rotacaoDireitaEsquerda(No *no) {
    no->direita = rotacaoDireita(no->direita);
    return rotacaoEsquerda(no);
}

// ====================================================================
// OPERAÇÕES DA ÁRVORE AVL
// ====================================================================

/**
 * Cria um novo nó com o contato fornecido
 * Inicializa ponteiros como NULL e altura como 1
 */
No* criarNo(Contato contato) {
    No *novoNo = (No*)malloc(sizeof(No));
    if (novoNo == NULL) {
        printf("\n[ERRO] Falha na alocação de memória!\n");
        return NULL;
    }
    
    novoNo->contato = contato;
    novoNo->esquerda = NULL;
    novoNo->direita = NULL;
    novoNo->altura = 1; // Nó folha tem altura 1
    
    return novoNo;
}

/**
 * Balanceia a árvore após inserção ou remoção
 * Verifica o fator de balanceamento e aplica as rotações necessárias
 */
No* balancear(No *no) {
    if (no == NULL)
        return no;

    // Atualiza a altura do nó atual
    atualizarAltura(no);

    // Calcula o fator de balanceamento
    int fb = fatorBalanceamento(no);

    // Caso 1: Desbalanceamento Esquerda-Esquerda (LL)
    if (fb > 1 && fatorBalanceamento(no->esquerda) >= 0) {
        return rotacaoDireita(no);
    }

    // Caso 2: Desbalanceamento Direita-Direita (RR)
    if (fb < -1 && fatorBalanceamento(no->direita) <= 0) {
        return rotacaoEsquerda(no);
    }

    // Caso 3: Desbalanceamento Esquerda-Direita (LR)
    if (fb > 1 && fatorBalanceamento(no->esquerda) < 0) {
        return rotacaoEsquerdaDireita(no);
    }

    // Caso 4: Desbalanceamento Direita-Esquerda (RL)
    if (fb < -1 && fatorBalanceamento(no->direita) > 0) {
        return rotacaoDireitaEsquerda(no);
    }

    return no; // Nó já está balanceado
}

/**
 * Insere um novo contato na árvore AVL
 * Mantém a propriedade de BST e balanceamento automático
 */
No* inserir(No *raiz, Contato contato) {
    // Passo 1: Inserção normal de BST
    if (raiz == NULL) {
        return criarNo(contato);
    }

    int comparacao = strcmp(contato.nome, raiz->contato.nome);

    if (comparacao < 0) {
        raiz->esquerda = inserir(raiz->esquerda, contato);
    } else if (comparacao > 0) {
        raiz->direita = inserir(raiz->direita, contato);
    } else {
        // Nome já existe - não permite duplicatas
        printf("\n[AVISO] Contato '%s' já existe na agenda!\n", contato.nome);
        return raiz;
    }

    // Passo 2: Balanceia a árvore
    return balancear(raiz);
}

/**
 * Encontra o nó com o menor valor (mais à esquerda)
 * Usado na remoção para encontrar o sucessor in-order
 */
No* encontrarMinimo(No *no) {
    No *atual = no;
    while (atual->esquerda != NULL) {
        atual = atual->esquerda;
    }
    return atual;
}

/**
 * Remove um contato da árvore AVL pelo nome
 * Mantém a propriedade de BST e balanceamento automático
 */
No* remover(No *raiz, char *nome, int *removido) {
    if (raiz == NULL) {
        *removido = 0;
        return raiz;
    }

    int comparacao = strcmp(nome, raiz->contato.nome);

    // Passo 1: Busca o nó a ser removido
    if (comparacao < 0) {
        raiz->esquerda = remover(raiz->esquerda, nome, removido);
    } else if (comparacao > 0) {
        raiz->direita = remover(raiz->direita, nome, removido);
    } else {
        // Nó encontrado - executa a remoção
        *removido = 1;

        // Caso 1: Nó com apenas um filho ou nenhum filho
        if (raiz->esquerda == NULL || raiz->direita == NULL) {
            No *temp = raiz->esquerda ? raiz->esquerda : raiz->direita;

            if (temp == NULL) {
                // Nenhum filho
                temp = raiz;
                raiz = NULL;
            } else {
                // Um filho
                *raiz = *temp; // Copia o conteúdo do filho
            }
            free(temp);
        } else {
            // Caso 2: Nó com dois filhos
            // Encontra o sucessor in-order (menor da subárvore direita)
            No *temp = encontrarMinimo(raiz->direita);
            raiz->contato = temp->contato; // Copia os dados do sucessor
            raiz->direita = remover(raiz->direita, temp->contato.nome, removido);
        }
    }

    if (raiz == NULL)
        return raiz;

    // Passo 2: Balanceia a árvore
    return balancear(raiz);
}

/**
 * Busca um contato exato pelo nome
 * Retorna o nó encontrado ou NULL se não existir
 */
No* buscar(No *raiz, char *nome) {
    if (raiz == NULL)
        return NULL;

    int comparacao = strcmp(nome, raiz->contato.nome);

    if (comparacao == 0) {
        return raiz; // Contato encontrado
    } else if (comparacao < 0) {
        return buscar(raiz->esquerda, nome);
    } else {
        return buscar(raiz->direita, nome);
    }
}

/**
 * Busca contatos por prefixo (BÔNUS)
 * Lista todos os contatos cujos nomes começam com o prefixo fornecido
 */
void buscarPorPrefixo(No *raiz, char *prefixo, int *encontrados) {
    if (raiz == NULL)
        return;

    // Percurso in-order para manter ordem alfabética
    buscarPorPrefixo(raiz->esquerda, prefixo, encontrados);

    // Verifica se o nome atual começa com o prefixo
    if (strncmp(raiz->contato.nome, prefixo, strlen(prefixo)) == 0) {
        if (*encontrados == 0) {
            printf("\n╔════════════════════════════════════════════════════════════════╗\n");
            printf("║           CONTATOS ENCONTRADOS COM PREFIXO '%s'", prefixo);
            for (int i = strlen(prefixo); i < 17; i++) printf(" ");
            printf("║\n");
            printf("╠════════════════════════════════════════════════════════════════╣\n");
        }
        printf("║ Nome:     %-50s ║\n", raiz->contato.nome);
        printf("║ Telefone: %-50s ║\n", raiz->contato.telefone);
        printf("║ Email:    %-50s ║\n", raiz->contato.email);
        printf("╠════════════════════════════════════════════════════════════════╣\n");
        (*encontrados)++;
    }

    buscarPorPrefixo(raiz->direita, prefixo, encontrados);
}

/**
 * Lista todos os contatos em ordem alfabética (percurso in-order)
 */
void listarContatos(No *raiz, int *total) {
    if (raiz == NULL)
        return;

    listarContatos(raiz->esquerda, total);

    if (*total == 0) {
        printf("\n╔════════════════════════════════════════════════════════════════╗\n");
        printf("║                    TODOS OS CONTATOS                           ║\n");
        printf("╠════════════════════════════════════════════════════════════════╣\n");
    }

    printf("║ [%03d] %-56s ║\n", (*total) + 1, raiz->contato.nome);
    printf("║       Telefone: %-46s ║\n", raiz->contato.telefone);
    printf("║       Email:    %-46s ║\n", raiz->contato.email);
    printf("╠════════════════════════════════════════════════════════════════╣\n");
    (*total)++;

    listarContatos(raiz->direita, total);
}

/**
 * Libera toda a memória alocada pela árvore
 * Usa percurso pós-order para liberar filhos antes do pai
 */
void liberarArvore(No *raiz) {
    if (raiz == NULL)
        return;

    liberarArvore(raiz->esquerda);
    liberarArvore(raiz->direita);
    free(raiz);
}

// ====================================================================
// PERSISTÊNCIA DE DADOS (ARQUIVO)
// ====================================================================

/**
 * Salva a árvore em arquivo usando percurso pré-order
 */
void salvarEmArquivo(No *raiz, FILE *arquivo) {
    if (raiz == NULL)
        return;

    fprintf(arquivo, "%s|%s|%s\n", 
            raiz->contato.nome, 
            raiz->contato.telefone, 
            raiz->contato.email);

    salvarEmArquivo(raiz->esquerda, arquivo);
    salvarEmArquivo(raiz->direita, arquivo);
}

/**
 * Salva todos os contatos da agenda no arquivo
 */
void salvarAgenda(No *raiz) {
    FILE *arquivo = fopen(ARQUIVO_DADOS, "w");
    if (arquivo == NULL) {
        printf("\n[ERRO] Não foi possível salvar a agenda!\n");
        return;
    }

    salvarEmArquivo(raiz, arquivo);
    fclose(arquivo);
}

/**
 * Carrega os contatos do arquivo e reconstrói a árvore AVL
 */
No* carregarAgenda() {
    FILE *arquivo = fopen(ARQUIVO_DADOS, "r");
    if (arquivo == NULL) {
        return NULL; // Arquivo não existe (primeira execução)
    }

    No *raiz = NULL;
    Contato contato;
    char linha[300];

    while (fgets(linha, sizeof(linha), arquivo)) {
        // Remove o \n do final
        linha[strcspn(linha, "\n")] = 0;

        // Separa os campos usando '|' como delimitador
        char *token = strtok(linha, "|");
        if (token != NULL) {
            strcpy(contato.nome, token);
            token = strtok(NULL, "|");
            if (token != NULL) {
                strcpy(contato.telefone, token);
                token = strtok(NULL, "|");
                if (token != NULL) {
                    strcpy(contato.email, token);
                    raiz = inserir(raiz, contato);
                }
            }
        }
    }

    fclose(arquivo);
    return raiz;
}

// ====================================================================
// INTERFACE DO USUÁRIO
// ====================================================================

/**
 * Limpa a tela do terminal (multiplataforma)
 */
void limparTela() {
    #ifdef _WIN32
        system("cls");
    #else
        system("clear");
    #endif
}

/**
 * Exibe o cabeçalho do programa
 */
void exibirCabecalho() {
    printf("\n");
    printf("╔════════════════════════════════════════════════════════════════╗\n");
    printf("║                                                                ║\n");
    printf("║               AGENDA TELEFÔNICA - ÁRVORE AVL                   ║\n");
    printf("║                                                                ║\n");
    printf("║          Trabalho Prático - Estruturas de Dados II             ║\n");
    printf("║                                                                ║\n");
    printf("╚════════════════════════════════════════════════════════════════╝\n");
}

/**
 * Exibe o menu principal
 */
void exibirMenu() {
    printf("\n");
    printf("╔════════════════════════════════════════════════════════════════╗\n");
    printf("║                        MENU PRINCIPAL                          ║\n");
    printf("╠════════════════════════════════════════════════════════════════╣\n");
    printf("║  [1] Inserir novo contato                                      ║\n");
    printf("║  [2] Remover contato                                           ║\n");
    printf("║  [3] Buscar contato exato                                      ║\n");
    printf("║  [4] Buscar por prefixo (BÔNUS)                                ║\n");
    printf("║  [5] Listar todos os contatos                                  ║\n");
    printf("║  [6] Sair e salvar                                             ║\n");
    printf("╚════════════════════════════════════════════════════════════════╝\n");
    printf("\n  Escolha uma opção: ");
}

/**
 * Aguarda o usuário pressionar Enter
 */
void pausar() {
    printf("\n  Pressione ENTER para continuar...");
    while (getchar() != '\n');
    getchar();
}

/**
 * Função principal
 */
int main() {
    No *raiz = NULL;
    int opcao;

    // Carrega os contatos salvos anteriormente
    raiz = carregarAgenda();

    while (1) {
        limparTela();
        exibirCabecalho();
        exibirMenu();
        scanf("%d", &opcao);
        while (getchar() != '\n'); // Limpa o buffer

        switch (opcao) {
            case 1: { // Inserir novo contato
                limparTela();
                exibirCabecalho();
                printf("\n╔════════════════════════════════════════════════════════════════╗\n");
                printf("║                     INSERIR NOVO CONTATO                       ║\n");
                printf("╚════════════════════════════════════════════════════════════════╝\n");

                Contato novoContato;
                printf("\n  Nome: ");
                fgets(novoContato.nome, MAX_NOME, stdin);
                novoContato.nome[strcspn(novoContato.nome, "\n")] = 0;

                printf("  Telefone: ");
                fgets(novoContato.telefone, MAX_TELEFONE, stdin);
                novoContato.telefone[strcspn(novoContato.telefone, "\n")] = 0;

                printf("  Email: ");
                fgets(novoContato.email, MAX_EMAIL, stdin);
                novoContato.email[strcspn(novoContato.email, "\n")] = 0;

                raiz = inserir(raiz, novoContato);
                printf("\n  [SUCESSO] Contato inserido com sucesso!\n");
                salvarAgenda(raiz);
                pausar();
                break;
            }

            case 2: { // Remover contato
                limparTela();
                exibirCabecalho();
                printf("\n╔════════════════════════════════════════════════════════════════╗\n");
                printf("║                       REMOVER CONTATO                          ║\n");
                printf("╚════════════════════════════════════════════════════════════════╝\n");

                char nome[MAX_NOME];
                printf("\n  Digite o nome do contato a remover: ");
                fgets(nome, MAX_NOME, stdin);
                nome[strcspn(nome, "\n")] = 0;

                int removido = 0;
                raiz = remover(raiz, nome, &removido);

                if (removido) {
                    printf("\n  [SUCESSO] Contato '%s' removido com sucesso!\n", nome);
                    salvarAgenda(raiz);
                } else {
                    printf("\n  [AVISO] Contato '%s' não encontrado!\n", nome);
                }
                pausar();
                break;
            }

            case 3: { // Buscar contato exato
                limparTela();
                exibirCabecalho();
                printf("\n╔════════════════════════════════════════════════════════════════╗\n");
                printf("║                      BUSCAR CONTATO EXATO                      ║\n");
                printf("╚════════════════════════════════════════════════════════════════╝\n");

                char nome[MAX_NOME];
                printf("\n  Digite o nome completo: ");
                fgets(nome, MAX_NOME, stdin);
                nome[strcspn(nome, "\n")] = 0;

                No *encontrado = buscar(raiz, nome);
                if (encontrado != NULL) {
                    printf("\n╔════════════════════════════════════════════════════════════════╗\n");
                    printf("║                     CONTATO ENCONTRADO                         ║\n");
                    printf("╠════════════════════════════════════════════════════════════════╣\n");
                    printf("║ Nome:     %-50s ║\n", encontrado->contato.nome);
                    printf("║ Telefone: %-50s ║\n", encontrado->contato.telefone);
                    printf("║ Email:    %-50s ║\n", encontrado->contato.email);
                    printf("╚════════════════════════════════════════════════════════════════╝\n");
                } else {
                    printf("\n  [AVISO] Contato '%s' não encontrado!\n", nome);
                }
                pausar();
                break;
            }

            case 4: { // Buscar por prefixo (BÔNUS)
                limparTela();
                exibirCabecalho();
                printf("\n╔════════════════════════════════════════════════════════════════╗\n");
                printf("║                    BUSCAR POR PREFIXO                          ║\n");
                printf("╚════════════════════════════════════════════════════════════════╝\n");

                char prefixo[MAX_NOME];
                printf("\n  Digite o prefixo (ex: Mar): ");
                fgets(prefixo, MAX_NOME, stdin);
                prefixo[strcspn(prefixo, "\n")] = 0;

                int encontrados = 0;
                buscarPorPrefixo(raiz, prefixo, &encontrados);

                if (encontrados > 0) {
                    printf("║ Total: %d contato(s) encontrado(s)                             ║\n", encontrados);
                    printf("╚════════════════════════════════════════════════════════════════╝\n");
                } else {
                    printf("\n  [AVISO] Nenhum contato encontrado com prefixo '%s'!\n", prefixo);
                }
                pausar();
                break;
            }

            case 5: { // Listar todos os contatos
                limparTela();
                exibirCabecalho();

                int total = 0;
                listarContatos(raiz, &total);

                if (total > 0) {
                    printf("║ Total: %d contato(s) na agenda                                 ║\n", total);
                    printf("╚════════════════════════════════════════════════════════════════╝\n");
                } else {
                    printf("\n  [AVISO] A agenda está vazia!\n");
                }
                pausar();
                break;
            }

            case 6: { // Sair e salvar
                salvarAgenda(raiz);
                liberarArvore(raiz);
                
                limparTela();
                exibirCabecalho();
                printf("\n╔════════════════════════════════════════════════════════════════╗\n");
                printf("║                                                                ║\n");
                printf("║          Agenda salva com sucesso!                             ║\n");
                printf("║                                                                ║\n");
                printf("╚════════════════════════════════════════════════════════════════╝\n\n");
                return 0;
            }

            default:
                printf("\n  [ERRO] Opção inválida! Tente novamente.\n");
                pausar();
        }
    }

    return 0;
}
