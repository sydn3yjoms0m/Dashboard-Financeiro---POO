import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Importações das nossas camadas de lógica
from modelos import Entrada, Despesa
from json_gerente import GerenciadorJSON

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppFinancas(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard Fina")
        
        # 💻 AJUSTE NATIVO: Inicia o aplicativo maximizado no monitor de forma responsiva
        self.state('zoomed') 

        # Inicializa a persistência e carrega os dados salvos
        self.gerenciador = GerenciadorJSON()
        self.carteira = self.gerenciador.carregar()

        # Configuração do Grid Principal: 3 colunas idênticas e ajustáveis
        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="colunas")
        self.grid_rowconfigure(0, weight=1)

        # ================= COLUNA 1: GRÁFICOS (ESQUERDA) =================
        self.frame_esquerda = ctk.CTkFrame(self, fg_color="#181818", corner_radius=15)
        self.frame_esquerda.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
        self.frame_esquerda.grid_rowconfigure((0, 1), weight=1) # Duas linhas para dividir os gráficos
        self.frame_esquerda.grid_columnconfigure(0, weight=1)

        # ================= COLUNA 2: AÇÕES E SALDO (MEIO) =================
        self.frame_meio = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_meio.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        self.frame_meio.grid_rowconfigure(0, weight=0) # Saldo fixo em cima
        self.frame_meio.grid_rowconfigure(1, weight=1) # Formulário estica embaixo
        self.frame_meio.grid_columnconfigure(0, weight=1)

        # Card de Saldo
        self.frame_saldo = ctk.CTkFrame(self.frame_meio, fg_color="#242424", height=100, corner_radius=12)
        self.frame_saldo.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        self.lbl_saldo_titulo = ctk.CTkLabel(self.frame_saldo, text="SALDO ATUAL DISPONÍVEL", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_saldo_titulo.pack(pady=(15, 2))
        self.lbl_saldo_valor = ctk.CTkLabel(self.frame_saldo, text="R$ 0.00", font=ctk.CTkFont(size=28, weight="bold"), text_color="#deff9a")
        self.lbl_saldo_valor.pack(pady=(0, 15))

        # Card de Formulário
        self.frame_form = ctk.CTkFrame(self.frame_meio, fg_color="#181818", corner_radius=15)
        self.frame_form.grid(row=1, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.frame_form, text="Nova Transação", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        self.txt_desc = ctk.CTkEntry(self.frame_form, placeholder_text="Descrição (Ex: Notebook, Salário)")
        self.txt_desc.pack(fill="x", padx=25, pady=8)

        self.cb_tipo = ctk.CTkOptionMenu(self.frame_form, values=["Entrada", "Despesa"])
        self.cb_tipo.pack(fill="x", padx=25, pady=8)

        self.cb_cat = ctk.CTkOptionMenu(self.frame_form, values=["Alimentação", "Moradia", "Lazer", "Renda", "Outros"])
        self.cb_cat.pack(fill="x", padx=25, pady=8)

        self.txt_valor = ctk.CTkEntry(self.frame_form, placeholder_text="Valor (R$)")
        self.txt_valor.pack(fill="x", padx=25, pady=8)

        self.btn_salvar = ctk.CTkButton(self.frame_form, text="Registrar Movimentação", command=self.adicionar, fg_color="#16a085", hover_color="#148f77")
        self.btn_salvar.pack(fill="x", padx=25, pady=25)

        # ================= COLUNA 3: HISTÓRICO (DIREITA) =================
        self.frame_direita = ctk.CTkFrame(self, fg_color="#181818", corner_radius=15)
        self.frame_direita.grid(row=0, column=2, padx=15, pady=15, sticky="nsew")
        
        ctk.CTkLabel(self.frame_direita, text="Histórico de Caixa", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)
        
        self.scroll_historico = ctk.CTkScrollableFrame(self.frame_direita, fg_color="transparent")
        self.scroll_historico.pack(fill="both", expand=True, padx=10, pady=10)

        # Prepara a renderização dos gráficos
        self.inicializar_graficos()
        self.atualizar_tela()

    def adicionar(self):
        desc = self.txt_desc.get()
        tipo = self.cb_tipo.get()
        cat = self.cb_cat.get()
        val_str = self.txt_valor.get()

        if desc and val_str:
            try:
                valor = float(val_str.replace(",", "."))
                
                # Instanciação correta aplicando Polimorfismo baseado na escolha do usuário
                if tipo == "Entrada":
                    nova_transacao = Entrada(desc, valor, cat)
                else:
                    nova_transacao = Despesa(desc, valor, cat)

                self.carteira.adicionar_transacao(nova_transacao)
                self.gerenciador.salvar(self.carteira) # Salvamento em tempo real

                # Limpeza de campos
                self.txt_desc.delete(0, tk.END)
                self.txt_valor.delete(0, tk.END)

                self.atualizar_tela()
            except ValueError:
                pass # Evita que o app quebre se digitarem texto no valor

    def atualizar_tela(self):
        # Atualiza Card de Saldo
        saldo = self.carteira.obter_saldo_total()
        cor_saldo = "#deff9a" if saldo >= 0 else "#ff6b6b"
        self.lbl_saldo_valor.configure(text=f"R$ {saldo:.2f}", text_color=cor_saldo)

        # Atualiza Lista de Histórico
        for widget in self.scroll_historico.winfo_children():
            widget.destroy()

        for t in reversed(self.carteira.transacoes):
            cor = "#2ecc71" if isinstance(t, Entrada) else "#e74c3c"
            sinal = "+" if isinstance(t, Entrada) else "-"
            
            box = ctk.CTkFrame(self.scroll_historico, fg_color="#252525")
            box.pack(fill="x", pady=4, padx=5)
            
            ctk.CTkLabel(box, text=f"{t.descricao} [{t.categoria}]", font=ctk.CTkFont(size=12)).pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(box, text=f"{sinal} R$ {t.valor:.2f}", text_color=cor, font=ctk.CTkFont(size=12, weight="bold")).pack(side="right", padx=10, pady=5)

        # Re-renderiza os dois gráficos de pizza
        self.atualizar_graficos()

    def inicializar_graficos(self):
        # Configura as duas figuras independentes do Matplotlib acopladas aos seus respectivos frames
        self.fig1 = Figure(figsize=(3, 3), facecolor='#181818')
        self.ax1 = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.frame_esquerda)
        self.canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.fig2 = Figure(figsize=(3, 3), facecolor='#181818')
        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.frame_esquerda)
        self.canvas2.get_tk_widget().grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def atualizar_graficos(self):
        # --- GRÁFICO 1: Despesas por Categoria ---
        self.ax1.clear()
        despesas_cat = {}
        for t in self.carteira.transacoes:
            if isinstance(t, Despesa):
                despesas_cat[t.categoria] = despesas_cat.get(t.categoria, 0) + t.valor

        if not despesas_cat:
            self.ax1.text(0.5, 0.5, "Sem despesas registradas", color="white", ha="center", va="center")
            self.ax1.axis('off')
        else:
            self.ax1.pie(list(despesas_cat.values()), labels=list(despesas_cat.keys()), autopct='%1.1f%%',
                         textprops={'color': "white", 'fontsize': 8}, colors=['#e74c3c', '#3498db', '#9b59b6', '#e67e22', '#f1c40f'])
            self.ax1.set_title("Distribuição de Despesas", color="white", fontsize=10, weight="bold")
            self.ax1.axis('equal')
        self.canvas1.draw()

        # --- GRÁFICO 2: Orçamento vs Sobra ---
        self.ax2.clear()
        entradas = self.carteira.obter_total_entradas()
        despesas = self.carteira.obter_total_despesas()
        sobra = entradas - despesas

        if entradas == 0:
            self.ax2.text(0.5, 0.5, "Aguardando receitas...", color="white", ha="center", va="center")
            self.ax2.axis('off')
        elif sobra < 0:
            self.ax2.text(0.5, 0.5, "Orçamento Estourado! ⚠️", color="#e74c3c", ha="center", va="center", weight="bold")
            self.ax2.axis('off')
        else:
            valores = [despesas, sobra]
            labels = ['Gastou', 'Sobrou']
            self.ax2.pie(valores, labels=labels, autopct='%1.1f%%', textprops={'color': "white", 'fontsize': 8}, colors=['#ff6b6b', '#2ecc71'])
            self.ax2.set_title("Uso Total do Salário", color="white", fontsize=10, weight="bold")
            self.ax2.axis('equal')
        self.canvas2.draw()

if __name__ == "__main__":
    app = AppFinancas()
    app.mainloop()