import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional


# ==================== ESTRUTURA DA ÁRVORE AVL ====================

class Node:
    """Nó da Árvore AVL - representa um contato"""
    def __init__(self, nome: str, telefone: str):
        self.nome = nome
        self.telefone = telefone
        self.left: Optional['Node'] = None
        self.right: Optional['Node'] = None
        self.height = 1


class AVLTree:
    """Árvore AVL para Agenda Telefônica"""
    
    def __init__(self):
        self.root: Optional[Node] = None
        self.rotation_count = 0
    
    # ==================== FUNÇÕES AUXILIARES ====================
    
    def get_height(self, node: Optional[Node]) -> int:
        """Retorna a altura do nó (0 se for None)"""
        return node.height if node else 0
    
    def get_balance(self, node: Optional[Node]) -> int:
        """Calcula o fator de balanceamento"""
        return self.get_height(node.left) - self.get_height(node.right) if node else 0
    
    def update_height(self, node: Optional[Node]) -> None:
        """Atualiza a altura do nó"""
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
    
    # ==================== ROTAÇÕES ====================
    
    def rotate_right(self, z: Node) -> Node:
        """Rotação Simples à Direita (Caso LL)"""
        self.rotation_count += 1
        y = z.left
        T3 = y.right
        
        y.right = z
        z.left = T3
        
        self.update_height(z)
        self.update_height(y)
        
        return y
    
    def rotate_left(self, z: Node) -> Node:
        """Rotação Simples à Esquerda (Caso RR)"""
        self.rotation_count += 1
        y = z.right
        T2 = y.left
        
        y.left = z
        z.right = T2
        
        self.update_height(z)
        self.update_height(y)
        
        return y
    
    def rotate_left_right(self, z: Node) -> Node:
        """Rotação Dupla Esquerda-Direita (Caso LR)"""
        z.left = self.rotate_left(z.left)
        return self.rotate_right(z)
    
    def rotate_right_left(self, z: Node) -> Node:
        """Rotação Dupla Direita-Esquerda (Caso RL)"""
        z.right = self.rotate_right(z.right)
        return self.rotate_left(z)
    
    # ==================== INSERÇÃO ====================
    
    def insert(self, nome: str, telefone: str) -> None:
        """Insere um novo contato na árvore"""
        self.root = self._insert_recursive(self.root, nome, telefone)
    
    def _insert_recursive(self, node: Optional[Node], nome: str, telefone: str) -> Node:
        """Função recursiva de inserção com balanceamento"""
        
        # 1. Inserção BST padrão
        if not node:
            return Node(nome, telefone)
        
        if nome < node.nome:
            node.left = self._insert_recursive(node.left, nome, telefone)
        elif nome > node.nome:
            node.right = self._insert_recursive(node.right, nome, telefone)
        else:
            node.telefone = telefone
            return node
        
        # 2. Atualiza altura
        self.update_height(node)
        
        # 3. Calcula balanceamento
        balance = self.get_balance(node)
        
        # 4. Casos de rotação
        if balance > 1 and nome < node.left.nome:
            return self.rotate_right(node)
        
        if balance < -1 and nome > node.right.nome:
            return self.rotate_left(node)
        
        if balance > 1 and nome > node.left.nome:
            return self.rotate_left_right(node)
        
        if balance < -1 and nome < node.right.nome:
            return self.rotate_right_left(node)
        
        return node
    
    # ==================== BUSCA ====================
    
    def search(self, nome: str) -> Optional[Node]:
        """Busca um contato pelo nome"""
        return self._search_recursive(self.root, nome)
    
    def _search_recursive(self, node: Optional[Node], nome: str) -> Optional[Node]:
        """Função recursiva de busca"""
        if not node or node.nome == nome:
            return node
        
        if nome < node.nome:
            return self._search_recursive(node.left, nome)
        return self._search_recursive(node.right, nome)
    
    # ==================== REMOÇÃO ====================
    
    def delete(self, nome: str) -> None:
        """Remove um contato da árvore"""
        self.root = self._delete_recursive(self.root, nome)
    
    def _delete_recursive(self, node: Optional[Node], nome: str) -> Optional[Node]:
        """Função recursiva de remoção com balanceamento"""
        
        # 1. Remoção BST padrão
        if not node:
            return node
        
        if nome < node.nome:
            node.left = self._delete_recursive(node.left, nome)
        elif nome > node.nome:
            node.right = self._delete_recursive(node.right, nome)
        else:
            # Nó encontrado
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            # Nó com 2 filhos
            successor = self._find_min(node.right)
            node.nome = successor.nome
            node.telefone = successor.telefone
            node.right = self._delete_recursive(node.right, successor.nome)
        
        if not node:
            return node
        
        # 2. Atualiza altura
        self.update_height(node)
        
        # 3. Balanceamento
        balance = self.get_balance(node)
        
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)
        
        if balance > 1 and self.get_balance(node.left) < 0:
            return self.rotate_left_right(node)
        
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)
        
        if balance < -1 and self.get_balance(node.right) > 0:
            return self.rotate_right_left(node)
        
        return node
    
    def _find_min(self, node: Node) -> Node:
        """Encontra o nó com menor valor"""
        current = node
        while current.left:
            current = current.left
        return current
    
    # ==================== LISTAGEM ====================
    
    def get_all_contacts(self) -> list:
        """Retorna todos os contatos em ordem alfabética"""
        contacts = []
        self._in_order_traversal(self.root, contacts)
        return contacts
    
    def _in_order_traversal(self, node: Optional[Node], contacts: list) -> None:
        """Percurso in-order (esquerda -> raiz -> direita)"""
        if node:
            self._in_order_traversal(node.left, contacts)
            contacts.append({'nome': node.nome, 'telefone': node.telefone})
            self._in_order_traversal(node.right, contacts)
    
    def count(self) -> int:
        """Conta o número total de nós"""
        return self._count_nodes(self.root)
    
    def _count_nodes(self, node: Optional[Node]) -> int:
        """Conta recursivamente os nós"""
        if not node:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)
    
    # ==================== PERSISTÊNCIA (PRÉ-ORDEM) ====================
    
    def save_to_file(self, filename: str = "agenda.txt") -> bool:
        """Salva a árvore em arquivo usando percurso pré-ordem"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                self._pre_order_save(self.root, f)
            return True
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            return False
    
    def _pre_order_save(self, node: Optional[Node], file) -> None:
        """Percurso pré-ordem (raiz -> esquerda -> direita)"""
        if node:
            file.write(f"{node.nome}|{node.telefone}\n")
            self._pre_order_save(node.left, file)
            self._pre_order_save(node.right, file)
    
    def load_from_file(self, filename: str = "agenda.txt") -> bool:
        """Carrega a árvore de um arquivo"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        nome, telefone = line.split('|')
                        self.insert(nome, telefone)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"Erro ao carregar: {e}")
            return False


# ==================== INTERFACE GRÁFICA ====================

class AgendaGUI:
    """Interface Gráfica da Agenda Telefônica"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📱 Agenda Telefônica AVL")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Instância da árvore AVL
        self.agenda = AVLTree()
        
        # Estilo
        self.setup_styles()
        
        # Componentes da interface
        self.create_widgets()
        
        # Carrega dados automaticamente se existirem
        self.load_contacts()
        
        # Atualiza display
        self.refresh_display()
    
    def setup_styles(self):
        """Configura estilos da interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores
        bg_color = "#f0f0f0"
        primary_color = "#667eea"
        
        self.root.configure(bg=bg_color)
        
        style.configure('Title.TLabel', 
                       font=('Arial', 24, 'bold'),
                       background=bg_color,
                       foreground=primary_color)
        
        style.configure('Header.TLabel',
                       font=('Arial', 14, 'bold'),
                       background='white',
                       foreground=primary_color)
        
        style.configure('Stat.TLabel',
                       font=('Arial', 20, 'bold'),
                       background='white',
                       foreground=primary_color)
        
        style.configure('StatLabel.TLabel',
                       font=('Arial', 10),
                       background='white',
                       foreground='#666')
        
        style.configure('Primary.TButton',
                       font=('Arial', 10, 'bold'),
                       background=primary_color,
                       foreground='white')
    
    def create_widgets(self):
        """Cria todos os widgets da interface"""
        
        # ===== TÍTULO =====
        title_frame = tk.Frame(self.root, bg='#f0f0f0')
        title_frame.pack(pady=20)
        
        ttk.Label(title_frame, text="📱 Agenda Telefônica AVL", 
                 style='Title.TLabel').pack()
        tk.Label(title_frame, text="Sistema de contatos com balanceamento automático",
                font=('Arial', 10), bg='#f0f0f0', fg='#666').pack()
        
        # ===== ESTATÍSTICAS =====
        stats_frame = tk.Frame(self.root, bg='#f0f0f0')
        stats_frame.pack(pady=10, padx=20, fill='x')
        
        # Total de contatos
        stat1 = tk.Frame(stats_frame, bg='white', relief='raised', bd=2)
        stat1.pack(side='left', expand=True, fill='both', padx=5)
        self.total_label = ttk.Label(stat1, text="0", style='Stat.TLabel')
        self.total_label.pack(pady=(10, 0))
        ttk.Label(stat1, text="Total de Contatos", style='StatLabel.TLabel').pack(pady=(0, 10))
        
        # Altura da árvore
        stat2 = tk.Frame(stats_frame, bg='white', relief='raised', bd=2)
        stat2.pack(side='left', expand=True, fill='both', padx=5)
        self.height_label = ttk.Label(stat2, text="0", style='Stat.TLabel')
        self.height_label.pack(pady=(10, 0))
        ttk.Label(stat2, text="Altura da Árvore", style='StatLabel.TLabel').pack(pady=(0, 10))
        
        # Rotações
        stat3 = tk.Frame(stats_frame, bg='white', relief='raised', bd=2)
        stat3.pack(side='left', expand=True, fill='both', padx=5)
        self.rotation_label = ttk.Label(stat3, text="0", style='Stat.TLabel')
        self.rotation_label.pack(pady=(10, 0))
        ttk.Label(stat3, text="Rotações Realizadas", style='StatLabel.TLabel').pack(pady=(0, 10))
        
        # ===== CONTAINER PRINCIPAL =====
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(pady=10, padx=20, fill='both', expand=True)
        
        # ===== FORMULÁRIO =====
        form_frame = tk.Frame(main_container, bg='white', relief='raised', bd=2)
        form_frame.pack(side='left', fill='both', padx=(0, 10), expand=True)
        
        ttk.Label(form_frame, text="➕ Adicionar/Editar Contato", 
                 style='Header.TLabel').pack(pady=15, padx=15, anchor='w')
        
        # Nome
        tk.Label(form_frame, text="Nome:", font=('Arial', 10, 'bold'),
                bg='white').pack(pady=(10, 5), padx=15, anchor='w')
        self.nome_entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.nome_entry.pack(padx=15, fill='x')
        
        # Telefone
        tk.Label(form_frame, text="Telefone:", font=('Arial', 10, 'bold'),
                bg='white').pack(pady=(10, 5), padx=15, anchor='w')
        self.telefone_entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.telefone_entry.pack(padx=15, fill='x')
        
        # Botões do formulário
        btn_frame1 = tk.Frame(form_frame, bg='white')
        btn_frame1.pack(pady=15, padx=15, fill='x')
        
        tk.Button(btn_frame1, text="Adicionar", font=('Arial', 10, 'bold'),
                 bg='#667eea', fg='white', command=self.add_contact,
                 cursor='hand2', relief='flat', padx=20, pady=8).pack(side='left', expand=True, fill='x', padx=(0, 5))
        
        tk.Button(btn_frame1, text="Limpar", font=('Arial', 10, 'bold'),
                 bg='#e0e0e0', fg='#333', command=self.clear_form,
                 cursor='hand2', relief='flat', padx=20, pady=8).pack(side='left', expand=True, fill='x', padx=(5, 0))
        
        # Separador
        ttk.Separator(form_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Busca
        ttk.Label(form_frame, text="🔍 Buscar Contato", 
                 style='Header.TLabel').pack(pady=15, padx=15, anchor='w')
        
        tk.Label(form_frame, text="Nome para buscar:", font=('Arial', 10, 'bold'),
                bg='white').pack(pady=(10, 5), padx=15, anchor='w')
        self.search_entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.search_entry.pack(padx=15, fill='x')
        
        tk.Button(form_frame, text="Buscar", font=('Arial', 10, 'bold'),
                 bg='#667eea', fg='white', command=self.search_contact,
                 cursor='hand2', relief='flat', padx=20, pady=8).pack(pady=15, padx=15, fill='x')
        
        # ===== LISTA DE CONTATOS =====
        list_frame = tk.Frame(main_container, bg='white', relief='raised', bd=2)
        list_frame.pack(side='left', fill='both', expand=True)
        
        ttk.Label(list_frame, text="📋 Lista de Contatos", 
                 style='Header.TLabel').pack(pady=15, padx=15, anchor='w')
        
        # Treeview para lista
        tree_container = tk.Frame(list_frame, bg='white')
        tree_container.pack(pady=(0, 15), padx=15, fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_container)
        scrollbar.pack(side='right', fill='y')
        
        self.tree = ttk.Treeview(tree_container, columns=('Nome', 'Telefone'),
                                 show='headings', yscrollcommand=scrollbar.set,
                                 height=10)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Telefone', text='Telefone')
        self.tree.column('Nome', width=200)
        self.tree.column('Telefone', width=150)
        
        # Botões de ação
        btn_frame2 = tk.Frame(list_frame, bg='white')
        btn_frame2.pack(pady=(0, 15), padx=15, fill='x')
        
        tk.Button(btn_frame2, text="✏️ Editar", font=('Arial', 9, 'bold'),
                 bg='#e0e0e0', fg='#333', command=self.edit_contact,
                 cursor='hand2', relief='flat', padx=15, pady=6).pack(side='left', expand=True, fill='x', padx=2)
        
        tk.Button(btn_frame2, text="🗑️ Excluir", font=('Arial', 9, 'bold'),
                 bg='#ff4757', fg='white', command=self.delete_contact,
                 cursor='hand2', relief='flat', padx=15, pady=6).pack(side='left', expand=True, fill='x', padx=2)
        
        # ===== BARRA DE AÇÕES =====
        action_frame = tk.Frame(self.root, bg='#f0f0f0')
        action_frame.pack(pady=(10, 20), padx=20, fill='x')
        
        tk.Button(action_frame, text="💾 Salvar Dados", font=('Arial', 10, 'bold'),
                 bg='#2ecc71', fg='white', command=self.save_contacts,
                 cursor='hand2', relief='flat', padx=20, pady=10).pack(side='left', expand=True, fill='x', padx=2)
        
        tk.Button(action_frame, text="📂 Carregar Dados", font=('Arial', 10, 'bold'),
                 bg='#3498db', fg='white', command=self.load_contacts,
                 cursor='hand2', relief='flat', padx=20, pady=10).pack(side='left', expand=True, fill='x', padx=2)
        
        tk.Button(action_frame, text="📥 Exportar TXT", font=('Arial', 10, 'bold'),
                 bg='#9b59b6', fg='white', command=self.export_data,
                 cursor='hand2', relief='flat', padx=20, pady=10).pack(side='left', expand=True, fill='x', padx=2)
        
        tk.Button(action_frame, text="🗑️ Limpar Tudo", font=('Arial', 10, 'bold'),
                 bg='#e74c3c', fg='white', command=self.clear_all,
                 cursor='hand2', relief='flat', padx=20, pady=10).pack(side='left', expand=True, fill='x', padx=2)
    
    # ==================== MÉTODOS DA INTERFACE ====================
    
    def add_contact(self):
        """Adiciona ou atualiza um contato"""
        nome = self.nome_entry.get().strip()
        telefone = self.telefone_entry.get().strip()
        
        if not nome or not telefone:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        self.agenda.insert(nome, telefone)
        messagebox.showinfo("Sucesso", f"Contato '{nome}' adicionado com sucesso!")
        self.clear_form()
        self.refresh_display()
    
    def clear_form(self):
        """Limpa o formulário"""
        self.nome_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.nome_entry.focus()
    
    def search_contact(self):
        """Busca um contato"""
        nome = self.search_entry.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "Digite um nome para buscar!")
            return
        
        result = self.agenda.search(nome)
        if result:
            messagebox.showinfo("Contato Encontrado", 
                              f"Nome: {result.nome}\nTelefone: {result.telefone}")
        else:
            messagebox.showwarning("Não Encontrado", 
                                  f"Contato '{nome}' não encontrado!")
    
    def edit_contact(self):
        """Edita o contato selecionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um contato para editar!")
            return
        
        item = self.tree.item(selected[0])
        nome, telefone = item['values']
        
        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, nome)
        self.telefone_entry.delete(0, tk.END)
        self.telefone_entry.insert(0, telefone)
        self.nome_entry.focus()
    
    def delete_contact(self):
        """Exclui o contato selecionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um contato para excluir!")
            return
        
        item = self.tree.item(selected[0])
        nome = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"Deseja realmente excluir '{nome}'?"):
            self.agenda.delete(nome)
            messagebox.showinfo("Sucesso", f"Contato '{nome}' excluído!")
            self.refresh_display()
    
    def refresh_display(self):
        """Atualiza a exibição"""
        # Limpa a lista
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adiciona contatos
        contacts = self.agenda.get_all_contacts()
        for contact in contacts:
            self.tree.insert('', 'end', values=(contact['nome'], contact['telefone']))
        
        # Atualiza estatísticas
        self.total_label.config(text=str(self.agenda.count()))
        self.height_label.config(text=str(self.agenda.get_height(self.agenda.root)))
        self.rotation_label.config(text=str(self.agenda.rotation_count))
    
    def save_contacts(self):
        """Salva contatos em arquivo"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de Texto", "*.txt"), ("Todos os Arquivos", "*.*")],
            initialfile="agenda.txt"
        )
        
        if filename:
            if self.agenda.save_to_file(filename):
                messagebox.showinfo("Sucesso", f"Dados salvos em '{filename}'!")
            else:
                messagebox.showerror("Erro", "Falha ao salvar os dados!")
    
    def load_contacts(self):
        """Carrega contatos de arquivo"""
        filename = filedialog.askopenfilename(
            filetypes=[("Arquivo de Texto", "*.txt"), ("Todos os Arquivos", "*.*")],
            initialfile="agenda.txt"
        )
        
        if filename:
            count_before = self.agenda.count()
            if self.agenda.load_from_file(filename):
                count_after = self.agenda.count()
                loaded = count_after - count_before
                messagebox.showinfo("Sucesso", f"{loaded} contatos carregados de '{filename}'!")
                self.refresh_display()
            else:
                messagebox.showwarning("Aviso", "Arquivo não encontrado ou inválido!")
    
    def export_data(self):
        """Exporta dados para TXT"""
        contacts = self.agenda.get_all_contacts()
        
        if not contacts:
            messagebox.showwarning("Aviso", "Nenhum contato para exportar!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de Texto", "*.txt")],
            initialfile="lista_contatos.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("=== AGENDA TELEFÔNICA AVL ===\n\n")
                    for contact in contacts:
                        f.write(f"{contact['nome']} | {contact['telefone']}\n")
                messagebox.showinfo("Sucesso", f"Lista exportada para '{filename}'!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao exportar: {e}")
    
    def clear_all(self):
        """Limpa todos os contatos"""
        if messagebox.askyesno("Confirmar", 
                              "⚠️ Deseja realmente excluir TODOS os contatos?\n"
                              "Esta ação não pode ser desfeita!"):
            self.agenda.root = None
            self.agenda.rotation_count = 0
            self.refresh_display()
            messagebox.showinfo("Sucesso", "Todos os contatos foram removidos!")


# ==================== EXECUÇÃO ====================

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaGUI(root)
    root.mainloop()
