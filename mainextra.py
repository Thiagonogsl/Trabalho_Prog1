import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime
import os
from PIL import Image  # Biblioteca para manipular imagens

# Configurações iniciais do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# ==============================================================================
#  BACKEND (Lógica de Dados)
# ==============================================================================
class Hospede:
    def __init__(self, nome, idade, telefone, pagamento, numero_quarto, contatos_emergencia, valor_diaria, checkin, checkout):
        self.nome = nome
        self.idade = idade
        self.telefone = telefone
        self.pagamento = pagamento
        self.quarto = int(numero_quarto)
        self.contatos_emergencia = contatos_emergencia
        self.valor_diaria = float(valor_diaria)
        self.checkin = checkin
        self.checkout = checkout

    def to_line(self) -> str:
        contatos_str = "[" + ",".join(self.contatos_emergencia) + "]"
        return f"{self.nome};{self.idade};{self.telefone};{self.pagamento};{self.quarto};{contatos_str};{self.valor_diaria};{self.checkin};{self.checkout}\n"

def carregar_dados(nome_arquivo):
    lista = []
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if not linha: continue
                partes = linha.split(';')
                if len(partes) < 9: continue
                
                extras = []
                try:
                    conteudo = partes[5].replace('[','').replace(']','')
                    if conteudo: extras = conteudo.split(',')
                except: pass

                h = Hospede(partes[0], partes[1], partes[2], partes[3], partes[4], extras, partes[6], partes[7], partes[8])
                lista.append(h)
    except FileNotFoundError:
        pass
    return lista

def salvar_dados(nome_arquivo, lista_hospedes):
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            for h in lista_hospedes:
                f.write(h.to_line())
        return True
    except Exception as e:
        return False

# ==============================================================================
#  FRONTEND (Interface Gráfica)
# ==============================================================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da Janela
        self.title("Sistema Hotel UFF - Dashboard")
        self.geometry("1100x650")
        
        # Dados
        self.arquivo_db = "dados_hotel.txt"
        self.hospedes = carregar_dados(self.arquivo_db)

        # Layout: Grid 1 linha x 2 colunas
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_sidebar()
        self.criar_area_principal()
        self.estilizar_tabela()
        self.atualizar_tabela()

    def criar_sidebar(self):
        # Frame Lateral (Esquerda)
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        # --- LÓGICA DO LOGO ---
        try:
            # Pega o caminho exato onde o script está rodando para achar a imagem
            caminho_script = os.path.dirname(os.path.abspath(__file__))
            caminho_imagem = os.path.join(caminho_script, "logo.png")
            
            imagem_carregada = ctk.CTkImage(
                light_image=Image.open(caminho_imagem),
                dark_image=Image.open(caminho_imagem),
                size=(150, 150) # Tamanho da imagem (Largura, Altura)
            )
            # Label COM imagem
            self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="", image=imagem_carregada)
            
        except Exception as e:
            # Se der erro (arquivo não existe), usa texto simples
            print(f"Aviso: Imagem não carregada. Erro: {e}")
            self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="HOTEL UFF", font=ctk.CTkFont(size=20, weight="bold"))
        # -----------------------

        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Inputs
        self.entry_nome = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Nome Completo")
        self.entry_nome.grid(row=1, column=0, padx=20, pady=10)

        self.entry_quarto = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Nº Quarto")
        self.entry_quarto.grid(row=2, column=0, padx=20, pady=10)

        self.entry_valor = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Valor Diária (R$)")
        self.entry_valor.grid(row=3, column=0, padx=20, pady=10)

        self.entry_checkin = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Check-in (DD/MM/AAAA)")
        self.entry_checkin.grid(row=4, column=0, padx=20, pady=10)
        self.entry_checkin.insert(0, datetime.datetime.now().strftime("%d/%m/%Y"))

        self.entry_checkout = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Check-out (DD/MM/AAAA)")
        self.entry_checkout.grid(row=5, column=0, padx=20, pady=10)

        # Botão Adicionar
        self.btn_add = ctk.CTkButton(self.sidebar_frame, text="Adicionar Hóspede", command=self.adicionar, fg_color="green", hover_color="darkgreen")
        self.btn_add.grid(row=6, column=0, padx=20, pady=20)

    def criar_area_principal(self):
        # Frame Principal (Direita)
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Barra de Topo
        self.top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.top_frame.pack(fill="x", pady=(0, 20))

        self.entry_busca = ctk.CTkEntry(self.top_frame, placeholder_text="Buscar por Nome ou Quarto...", width=300)
        self.entry_busca.pack(side="left", padx=(0, 10))

        self.btn_busca = ctk.CTkButton(self.top_frame, text="Buscar", width=100, command=self.buscar)
        self.btn_busca.pack(side="left", padx=5)

        self.btn_limpar = ctk.CTkButton(self.top_frame, text="Limpar", width=80, fg_color="gray", command=lambda: self.atualizar_tabela())
        self.btn_limpar.pack(side="left", padx=5)
        
        # Botões de Ação
        self.btn_save = ctk.CTkButton(self.top_frame, text="Salvar", command=self.salvar, fg_color="#1f538d")
        self.btn_save.pack(side="right", padx=5)
        
        self.btn_remove = ctk.CTkButton(self.top_frame, text="Remover", command=self.remover, fg_color="#b32d2d", hover_color="#802020")
        self.btn_remove.pack(side="right", padx=5)

        # Tabela (Treeview)
        self.tree_frame = ctk.CTkFrame(self.main_frame)
        self.tree_frame.pack(fill="both", expand=True)

        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side="right", fill="y")

        colunas = ("quarto", "nome", "checkin", "checkout", "valor")
        self.tree = ttk.Treeview(self.tree_frame, columns=colunas, show="headings", yscrollcommand=self.tree_scroll.set)
        
        self.tree_scroll.config(command=self.tree.yview)
        
        self.tree.heading("quarto", text="Quarto")
        self.tree.heading("nome", text="Nome Completo")
        self.tree.heading("checkin", text="Check-in")
        self.tree.heading("checkout", text="Check-out")
        self.tree.heading("valor", text="Diária (R$)")

        self.tree.column("quarto", width=80, anchor="center")
        self.tree.column("nome", width=350)
        self.tree.column("checkin", width=120, anchor="center")
        self.tree.column("checkout", width=120, anchor="center")
        self.tree.column("valor", width=120, anchor="e")

        self.tree.pack(fill="both", expand=True)

    def estilizar_tabela(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        fieldbackground="#2b2b2b",
                        rowheight=30,
                        font=("Arial", 11))
        
        style.configure("Treeview.Heading",
                        background="#1f538d",
                        foreground="white",
                        font=("Arial", 12, "bold"))
        
        style.map("Treeview", background=[('selected', '#1f6aa5')])

    def atualizar_tabela(self, lista_filtro=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        fonte = lista_filtro if lista_filtro is not None else self.hospedes
        for h in fonte:
            self.tree.insert("", "end", values=(h.quarto, h.nome, h.checkin, h.checkout, f"R$ {h.valor_diaria}"))

    def adicionar(self):
        nome = self.entry_nome.get()
        quarto = self.entry_quarto.get()
        valor = self.entry_valor.get()
        checkin = self.entry_checkin.get()
        checkout = self.entry_checkout.get()

        if not nome or not quarto or not valor:
            messagebox.showwarning("Aviso", "Preencha os campos obrigatórios!")
            return

        try:
            # Dados simplificados para interface rápida
            novo = Hospede(nome, 0, "N/A", "False", quarto, [], valor, checkin, checkout)
            self.hospedes.append(novo)
            self.atualizar_tabela()
            
            # Limpa campos
            self.entry_nome.delete(0, 'end')
            self.entry_quarto.delete(0, 'end')
            self.entry_valor.delete(0, 'end')
            
        except ValueError:
            messagebox.showerror("Erro", "Quarto e Valor devem ser numéricos.")

    def remover(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma linha para remover.")
            return
        
        item = self.tree.item(sel)
        quarto_alvo = str(item['values'][0])
        
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o quarto {quarto_alvo}?"):
            self.hospedes = [h for h in self.hospedes if str(h.quarto) != quarto_alvo]
            self.atualizar_tabela()

    def salvar(self):
        if salvar_dados(self.arquivo_db, self.hospedes):
            messagebox.showinfo("Sucesso", "Dados salvos no arquivo TXT!")
        else:
            messagebox.showerror("Erro", "Falha ao salvar.")

    def buscar(self):
        termo = self.entry_busca.get().lower()
        if not termo: return
        filtrados = [h for h in self.hospedes if termo in h.nome.lower() or termo in str(h.quarto)]
        self.atualizar_tabela(filtrados)

if __name__ == "__main__":
    app = App()
    app.mainloop()
