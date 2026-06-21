import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Importações das camadas de lógica
from json_gerente import GerenciadorJSON
from modelos import Despesa, Entrada

# Configurações Globais de Design do App
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AppFinancas(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Dashboard Finaceiro")
        
        # Inicia o aplicativo maximizado de forma responsiva
        self.state("zoomed")
        self.configure(fg_color="#0A0A0E")

        # Inicializa a persistência e carrega os dados salvos
        self.gerenciador = GerenciadorJSON()
        self.carteira = self.gerenciador.carregar()

        # Grid Principal: Linha 0 (Cards de Indicadores) | Linha 1 (3 Colunas de Trabalho)
        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure(1, weight=1)  
        self.grid_columnconfigure(0, weight=1)

        # =================================================================
        # TOP CARDS DE METRICAS (Visualização Rápida)
        # =================================================================
        self.frame_top_cards = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top_cards.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        self.frame_top_cards.grid_columnconfigure((0, 1, 2), weight=1, uniform="top_cards")

        # CARD: SALDO ATUAL
        self.card_saldo = ctk.CTkFrame(self.frame_top_cards, fg_color="#121218", corner_radius=16)
        self.card_saldo.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        ctk.CTkLabel(self.card_saldo, text="SALDO ATUAL", font=ctk.CTkFont(family="Arial", size=11, weight="bold"), text_color="#52526B").pack(pady=(15, 2))
        self.lbl_saldo_valor = ctk.CTkLabel(self.card_saldo, text="R$ 0.00", font=ctk.CTkFont(family="Arial", size=24, weight="bold"), text_color="#00ADB5")
        self.lbl_saldo_valor.pack(pady=(0, 15))

        # CARD: TOTAL DE ENTRADAS
        self.card_entradas = ctk.CTkFrame(self.frame_top_cards, fg_color="#121218", corner_radius=16)
        self.card_entradas.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        ctk.CTkLabel(self.card_entradas, text="TOTAL DE ENTRADAS", font=ctk.CTkFont(family="Arial", size=11, weight="bold"), text_color="#52526B").pack(pady=(15, 2))
        self.lbl_total_entradas = ctk.CTkLabel(self.card_entradas, text="R$ 0.00", font=ctk.CTkFont(family="Arial", size=24, weight="bold"), text_color="#2ECC71")
        self.lbl_total_entradas.pack(pady=(0, 15))

        # CARD: TOTAL DE GASTOS
        self.card_despesas = ctk.CTkFrame(self.frame_top_cards, fg_color="#121218", corner_radius=16)
        self.card_despesas.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
        ctk.CTkLabel(self.card_despesas, text="TOTAL DE GASTOS", font=ctk.CTkFont(family="Arial", size=11, weight="bold"), text_color="#52526B").pack(pady=(15, 2))
        self.lbl_total_despesas = ctk.CTkLabel(self.card_despesas, text="R$ 0.00", font=ctk.CTkFont(family="Arial", size=24, weight="bold"), text_color="#E74C3C")
        self.lbl_total_despesas.pack(pady=(0, 15))


        # =================================================================
        # DASHBOARD PRINCIPAL (3 Colunas)
        # =================================================================
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.main_container.grid_columnconfigure((0, 1, 2), weight=1, uniform="workspace")
        self.main_container.grid_rowconfigure(0, weight=1)

        # --- COLUNA 1: GESTÃO DE ENTRADAS (ESQUERDA) ---
        self.col_entradas = ctk.CTkFrame(self.main_container, fg_color="#121218", corner_radius=20)
        self.col_entradas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.col_entradas.grid_rowconfigure(0, weight=0) # Form
        self.col_entradas.grid_rowconfigure(1, weight=1) # Gráfico exclusivo
        self.col_entradas.grid_columnconfigure(0, weight=1)

        # Formulário de Entrada
        self.frame_form_entrada = ctk.CTkFrame(self.col_entradas, fg_color="transparent")
        self.frame_form_entrada.grid(row=0, column=0, sticky="ew", padx=20, pady=(25, 10))
        
        ctk.CTkLabel(self.frame_form_entrada, text="Nova Entrada / Receita", font=ctk.CTkFont(family="Arial", size=16, weight="bold"), text_color="#2ECC71").pack(anchor="w", padx=15, pady=(0, 15))
        
        self.txt_desc_entrada = ctk.CTkEntry(self.frame_form_entrada, placeholder_text="Origem (Ex: Salário, Freelance)", height=42, fg_color="#1A1A24", border_width=0, corner_radius=10)
        self.txt_desc_entrada.pack(fill="x", padx=15, pady=6)
        
        self.cb_cat_entrada = ctk.CTkOptionMenu(self.frame_form_entrada, values=["Renda", "Investimentos", "Outros"], height=42, fg_color="#1A1A24", button_color="#222230", corner_radius=10)
        self.cb_cat_entrada.pack(fill="x", padx=15, pady=6)
        
        self.txt_valor_entrada = ctk.CTkEntry(self.frame_form_entrada, placeholder_text="Valor Recebido R$", height=42, fg_color="#1A1A24", border_width=0, corner_radius=10)
        self.txt_valor_entrada.pack(fill="x", padx=15, pady=6)
        
        self.btn_salvar_entrada = ctk.CTkButton(self.frame_form_entrada, text="+ Inserir Receita", command=self.adicionar_entrada, height=45, fg_color="#2ECC71", hover_color="#229954", font=ctk.CTkFont(family="Arial", size=13, weight="bold"), corner_radius=10)
        self.btn_salvar_entrada.pack(fill="x", padx=15, pady=(15, 5))

        # Container do Gráfico de Entradas
        self.frame_grafico_entrada = ctk.CTkFrame(self.col_entradas, fg_color="transparent")
        self.frame_grafico_entrada.grid(row=1, column=0, sticky="nsew", padx=25, pady=25)


        # --- COLUNA 2: GESTÃO DE GASTOS / SAÍDAS (MEIO) ---
        self.col_gastos = ctk.CTkFrame(self.main_container, fg_color="#121218", corner_radius=20)
        self.col_gastos.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.col_gastos.grid_rowconfigure(0, weight=0) # Form
        self.col_gastos.grid_rowconfigure(1, weight=1) # Gráfico exclusivo
        self.col_gastos.grid_columnconfigure(0, weight=1)

        # Formulário de Gasto
        self.frame_form_gasto = ctk.CTkFrame(self.col_gastos, fg_color="transparent")
        self.frame_form_gasto.grid(row=0, column=0, sticky="ew", padx=20, pady=(25, 10))
        
        ctk.CTkLabel(self.frame_form_gasto, text="Novo Gasto / Despesa", font=ctk.CTkFont(family="Arial", size=16, weight="bold"), text_color="#E74C3C").pack(anchor="w", padx=15, pady=(0, 15))
        
        self.txt_desc_gasto = ctk.CTkEntry(self.frame_form_gasto, placeholder_text="Descrição (Ex: Aluguel, Mercado)", height=42, fg_color="#1A1A24", border_width=0, corner_radius=10)
        self.txt_desc_gasto.pack(fill="x", padx=15, pady=6)
        
        self.cb_cat_gasto = ctk.CTkOptionMenu(self.frame_form_gasto, values=["Alimentação", "Moradia", "Lazer", "Transporte", "Outros"], height=42, fg_color="#1A1A24", button_color="#222230", corner_radius=10)
        self.cb_cat_gasto.pack(fill="x", padx=15, pady=6)
        
        self.txt_valor_gasto = ctk.CTkEntry(self.frame_form_gasto, placeholder_text="Valor Gasto R$", height=42, fg_color="#1A1A24", border_width=0, corner_radius=10)
        self.txt_valor_gasto.pack(fill="x", padx=15, pady=6)
        
        self.btn_salvar_gasto = ctk.CTkButton(self.frame_form_gasto, text="- Inserir Despesa", command=self.adicionar_gasto, height=45, fg_color="#E74C3C", hover_color="#C0392B", font=ctk.CTkFont(family="Arial", size=13, weight="bold"), corner_radius=10)
        self.btn_salvar_gasto.pack(fill="x", padx=15, pady=(15, 5))

        # Container do Gráfico de Gastos
        self.frame_grafico_gasto = ctk.CTkFrame(self.col_gastos, fg_color="transparent")
        self.frame_grafico_gasto.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)


        # --- COLUNA 3: HISTÓRICO CONSOLIDADO (DIREITA) ---
        self.col_historico = ctk.CTkFrame(self.main_container, fg_color="#121218", corner_radius=20)
        self.col_historico.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.col_historico.grid_rowconfigure(0, weight=1)
        self.col_historico.grid_rowconfigure(1, weight=0)

        ctk.CTkLabel(self.col_historico, text="Histórico Geral", font=ctk.CTkFont(family="Arial", size=16, weight="bold"), text_color="#FFFFFF").pack(anchor="w", padx=35, pady=(30, 10))

        self.scroll_historico = ctk.CTkScrollableFrame(self.col_historico, fg_color="transparent")
        self.scroll_historico.pack(fill="both", expand=True, padx=20, pady=5)

        # Sistema de Exclusão integrado na base do histórico
        self.linha_apagar = ctk.CTkFrame(self.col_historico, fg_color="transparent")
        self.linha_apagar.pack(fill="x", padx=25, pady=25)

        self.txt_indice_apagar = ctk.CTkEntry(self.linha_apagar, placeholder_text="N° da linha para apagar", height=42, fg_color="#1A1A24", border_width=0, corner_radius=10)
        self.txt_indice_apagar.pack(side="left", fill="x", expand=True, padx=(0, 12))

        self.btn_apagar = ctk.CTkButton(self.linha_apagar, text="✕ Excluir", command=self.apagar_por_indice, height=42, fg_color="#3A1C1C", hover_color="#5C2525", text_color="#FF6B6B", font=ctk.CTkFont(family="Arial", size=12, weight="bold"), width=90, corner_radius=10)
        self.btn_apagar.pack(side="right")

        # Setup estrutural de gráficos e dados iniciais
        self.inicializar_graficos()
        self.atualizar_tela()

    def adicionar_entrada(self):
        # .get() pega o imput do usuário para realizar as operações.
        desc = self.txt_desc_entrada.get()
        cat = self.cb_cat_entrada.get()
        val_str = self.txt_valor_entrada.get()

        if desc and val_str:
            try:
                valor = float(val_str.replace(",", "."))
                nova_transacao = Entrada(desc, valor, cat)
                
                self.carteira.adicionar_transacao(nova_transacao)
                self.gerenciador.salvar(self.carteira)

                self.txt_desc_entrada.delete(0, tk.END)
                self.txt_valor_entrada.delete(0, tk.END)
                self.atualizar_tela()
            except ValueError:
                pass

    def adicionar_gasto(self):
        # .get() pega o imput do usuário para realizar as operações.
        desc = self.txt_desc_gasto.get()
        cat = self.cb_cat_gasto.get()
        val_str = self.txt_valor_gasto.get()

        if desc and val_str:
            try:
                valor = float(val_str.replace(",", "."))
                nova_transacao = Despesa(desc, valor, cat)
                
                self.carteira.adicionar_transacao(nova_transacao)
                self.gerenciador.salvar(self.carteira)

                self.txt_desc_gasto.delete(0, tk.END)
                self.txt_valor_gasto.delete(0, tk.END)
                self.atualizar_tela()
            except ValueError:
                pass

    def apagar_por_indice(self):
        entrada_usuario = self.txt_indice_apagar.get()

        if not entrada_usuario:
            messagebox.showwarning("Aviso", "Digite o número do item para apagar!")
            return

        try:
            numero_item = int(entrada_usuario)
            total_itens = len(self.carteira.transacoes)

            if 1 <= numero_item <= total_itens:
                indice_real = total_itens - numero_item
                self.carteira.transacoes.pop(indice_real)
                self.gerenciador.salvar(self.carteira)
                
                self.txt_indice_apagar.delete(0, tk.END)
                self.atualizar_tela()
                
                messagebox.showinfo("Sucesso", f"Item número {numero_item} apagado!")
            else:
                messagebox.showerror("Erro", "Número de item inválido.")
        except ValueError:
            messagebox.showerror("Erro", "Digite apenas números inteiros.")

    def atualizar_tela(self):
        # Captura e sincronização dos dados nas caixas de contabilidade do topo
        saldo = self.carteira.obter_saldo_total()
        entradas = self.carteira.obter_total_entradas()
        despesas = self.carteira.obter_total_despesas()

        cor_saldo = "#00ADB5" if saldo >= 0 else "#E74C3C"
        self.lbl_saldo_valor.configure(text=f"R$ {saldo:.2f}", text_color=cor_saldo)
        self.lbl_total_entradas.configure(text=f"R$ {entradas:.2f}")
        self.lbl_total_despesas.configure(text=f"R$ {despesas:.2f}")

        # Limpa e redesenha a Timeline do Histórico Geral
        for widget in self.scroll_historico.winfo_children():
            widget.destroy()

        for i, t in enumerate(reversed(self.carteira.transacoes), start=1):
            cor = "#2ECC71" if isinstance(t, Entrada) else "#E74C3C"
            sinal = "+" if isinstance(t, Entrada) else "-"

            box = ctk.CTkFrame(self.scroll_historico, fg_color="#1A1A24", corner_radius=10, height=45)
            box.pack(fill="x", pady=4, padx=2)

            ctk.CTkLabel(box, text=f"{i:02d}", font=ctk.CTkFont(family="Arial", size=11, weight="bold"), text_color="#00ADB5").pack(side="left", padx=(15, 5))
            ctk.CTkLabel(box, text=f"{t.descricao} • {t.categoria}", font=ctk.CTkFont(family="Arial", size=12, weight="normal"), text_color="#D1D1D6").pack(side="left", padx=5, pady=10)
            ctk.CTkLabel(box, text=f"{sinal} R$ {t.valor:.2f}", text_color=cor, font=ctk.CTkFont(family="Arial", size=12, weight="bold")).pack(side="right", padx=15, pady=10)

        self.atualizar_graficos()

    def inicializar_graficos(self):
        # Gráfico da esquerda acoplado em sua respectiva coluna (Entradas)
        self.fig1 = Figure(figsize=(3, 2.5), facecolor="#121218")
        self.ax1 = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.frame_grafico_entrada)
        self.canvas1.get_tk_widget().pack(fill="both", expand=True)

        # Gráfico do meio acoplado em sua respectiva coluna (Gastos)
        self.fig2 = Figure(figsize=(3, 2.5), facecolor="#121218")
        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.frame_grafico_gasto)
        self.canvas2.get_tk_widget().pack(fill="both", expand=True)

    def atualizar_graficos(self):
        # --- GRÁFICO 1 (LADO ENTRADAS): Balanço Geral / Saúde da Receita ---
        self.ax1.clear()
        entradas = self.carteira.obter_total_entradas()
        despesas = self.carteira.obter_total_despesas()
        sobra = entradas - despesas

        if entradas == 0:
            self.ax1.text(0.5, 0.5, "Sem fluxo de entrada ativo", color="#52526B", ha="center", va="center", fontsize=10)
            self.ax1.axis("off")
        elif sobra < 0:
            self.ax1.text(0.5, 0.5, "ALERTA: ORÇAMENTO NEGATIVO! ⚠️", color="#FF6B6B", ha="center", va="center", weight="bold", fontsize=10)
            self.ax1.axis("off")
        else:
            self.ax1.pie([despesas, sobra], labels=["Gasto Total", "Sobra em Caixa"], autopct="%1.1f%%", pctdistance=0.6, textprops={"color": "#D1D1D6", "fontsize": 8}, colors=["#FF6B6B", "#2ECC71"], wedgeprops={'edgecolor': '#121218', 'linewidth': 2})
            self.ax1.set_title("APROVEITAMENTO DAS RECEITAS", color="#52526B", fontsize=10, weight="bold", pad=12)
            self.ax1.axis("equal")

        self.fig1.tight_layout()
        self.canvas1.draw()

        # --- GRÁFICO 2 (LADO GASTOS): Detalhamento de Custos ---
        self.ax2.clear()
        despesas_cat = {}
        for t in self.carteira.transacoes:
            if isinstance(t, Despesa):
                despesas_cat[t.categoria] = despesas_cat.get(t.categoria, 0) + t.valor

        if not despesas_cat:
            self.ax2.text(0.5, 0.5, "Sem gastos catalogados", color="#52526B", ha="center", va="center", fontsize=10)
            self.ax2.axis("off")
        else:
            self.ax2.pie(list(despesas_cat.values()), labels=list(despesas_cat.keys()), autopct="%1.1f%%", pctdistance=0.6, textprops={"color": "#D1D1D6", "fontsize": 8}, colors=["#FF6B6B", "#4FACFE", "#B19FFB", "#F7B731", "#55EFC4"], wedgeprops={'edgecolor': '#121218', 'linewidth': 2})
            self.ax2.set_title("DISTRIBUIÇÃO DE DESPESAS", color="#52526B", fontsize=10, weight="bold", pad=12)
            self.ax2.axis("equal")

        self.fig1.tight_layout()
        self.canvas2.draw()


if __name__ == "__main__":
    app = AppFinancas()
    app.mainloop()