import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import json
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random




# Lista para armazenar histórico das simulações
historico = []
modo_escuro = False

# Função para calcular parcelas PRICE (juros compostos)
def calcular_price(valor, taxa_juros, parcelas):
    taxa = taxa_juros / 100
    if taxa == 0:
        valor_parcela = valor / parcelas
    else:
        valor_parcela = valor * (taxa * (1 + taxa) ** parcelas) / ((1 + taxa) ** parcelas - 1)
    total_pago = valor_parcela * parcelas
    total_juros = total_pago - valor
    return round(valor_parcela, 2), round(total_pago, 2), round(total_juros, 2)

# Função para calcular parcelas SAC (amortização constante)
def calcular_sac(valor, taxa_juros, parcelas):
    amortizacao = valor / parcelas
    saldo_devedor = valor
    total_pago = 0
    total_juros = 0
    for _ in range(parcelas):
        juros = saldo_devedor * (taxa_juros / 100)
        parcela = amortizacao + juros
        total_pago += parcela
        total_juros += juros
        saldo_devedor -= amortizacao
    parcela_media = total_pago / parcelas
    return round(parcela_media, 2), round(total_pago, 2), round(total_juros, 2)

# Salvar histórico como JSON
def salvar_historico_json():
    with open("historico_simulacoes.json", "w") as f:
        json.dump(historico, f, indent=4)
    messagebox.showinfo("Sucesso", "Histórico salvo em JSON com sucesso!")

# Salvar histórico como CSV
def salvar_historico_csv():
    with open("historico_simulacoes.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=historico[0].keys())
        writer.writeheader()
        writer.writerows(historico)
    messagebox.showinfo("Sucesso", "Histórico salvo em CSV com sucesso!")

# Exibir gráfico incorporado na interface
def exibir_grafico_embutido(janela):
    if not historico:
        messagebox.showwarning("Aviso", "Nenhuma simulação para exibir gráfico.")
        return

    indices = list(range(1, len(historico)+1))
    totais = [h["total"] for h in historico]
    juros = [h["juros_total"] for h in historico]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(indices, totais, label="Total Pago", marker='o')
    ax.plot(indices, juros, label="Juros Totais", marker='x')
    ax.set_title("Comparação: Total Pago vs Juros Totais")
    ax.set_xlabel("Simulação")
    ax.set_ylabel("Valor (R$)")
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Alternar modo escuro
def alternar_modo_escuro(root):
    global modo_escuro
    modo_escuro = not modo_escuro
    cor_fundo = "#2e2e2e" if modo_escuro else "#f0f0f0"
    cor_texto = "white" if modo_escuro else "black"
    root.configure(bg=cor_fundo)
    for widget in root.winfo_children():
        try:
            widget.configure(bg=cor_fundo, fg=cor_texto)
        except:
            pass

# Jogo simples: Adivinhe o número
def iniciar_jogo():
    janela = tk.Toplevel()
    janela.title("Jogo: Adivinhe o Número")
    janela.geometry("300x200")

    numero_secreto = random.randint(1, 100)

    tk.Label(janela, text="Adivinhe um número entre 1 e 100:").pack(pady=10)
    entrada = tk.Entry(janela)
    entrada.pack()
    resultado = tk.Label(janela, text="")
    resultado.pack(pady=5)

    def verificar():
        try:
            palpite = int(entrada.get())
            if palpite < numero_secreto:
                resultado.config(text="Muito baixo!")
            elif palpite > numero_secreto:
                resultado.config(text="Muito alto!")
            else:
                resultado.config(text="Parabéns! Você acertou!")
        except:
            resultado.config(text="Digite um número válido")

    tk.Button(janela, text="Verificar", command=verificar).pack(pady=5)
    tk.Button(janela, text="Sair", command=janela.destroy).pack(pady=5)

# Tela de simulação
def tela_simulacao():
    janela = tk.Toplevel()
    janela.title("Simulador de Financiamento")
    janela.geometry("400x500")

    moedas = {"BRL": "R$", "USD": "$", "EUR": "€"}
    moeda_var = tk.StringVar(value="BRL")

    def get_simulacao():
        tipo = tipo_var.get()
        if tipo == "PRICE":
            return calcular_price
        else:
            return calcular_sac

    tk.Label(janela, text="Valor do empréstimo:").pack()
    entry_valor = tk.Scale(janela, from_=1000, to=100000, orient="horizontal", resolution=100)
    entry_valor.pack()

    tk.Label(janela, text="Taxa de juros (% ao mês):").pack()
    entry_juros = tk.Scale(janela, from_=0, to=10, orient="horizontal", resolution=0.1)
    entry_juros.pack()

    tk.Label(janela, text="Número de parcelas:").pack()
    entry_parcelas = tk.Scale(janela, from_=1, to=120, orient="horizontal")
    entry_parcelas.pack()

    tk.Label(janela, text="Tipo de financiamento:").pack()
    tipo_var = tk.StringVar(value="PRICE")
    ttk.Combobox(janela, textvariable=tipo_var, values=["PRICE", "SAC"], state="readonly").pack()

    tk.Label(janela, text="Moeda:").pack()
    moeda_menu = ttk.Combobox(janela, textvariable=moeda_var, values=list(moedas.keys()), state="readonly")
    moeda_menu.pack()

    result_label = tk.Label(janela, text="", justify="left")
    result_label.pack(pady=10)

    def simular():
        valor = entry_valor.get()
        juros = entry_juros.get()
        qtd = entry_parcelas.get()
        moeda = moeda_var.get()
        funcao = get_simulacao()
        parcela, total, juros_total = funcao(valor, juros, qtd)
        resultado = (
            f"Parcela mensal: {moedas[moeda]} {parcela:.2f}\n"
            f"Total pago: {moedas[moeda]} {total:.2f}\n"
            f"Total de juros: {moedas[moeda]} {juros_total:.2f}"
        )
        result_label.config(text=resultado)
        historico.append({
            "valor": valor,
            "juros": juros,
            "parcelas": qtd,
            "tipo": tipo_var.get(),
            "moeda": moeda,
            "parcela": parcela,
            "total": total,
            "juros_total": juros_total
        })

    tk.Button(janela, text="Simular", command=simular).pack(pady=10)
    tk.Button(janela, text="Sair", command=janela.destroy).pack(pady=5)

# Tela de histórico
def tela_historico():
    janela = tk.Toplevel()
    janela.title("Histórico de Simulações")
    janela.geometry("900x500")

    if not historico:
        tk.Label(janela, text="Nenhuma simulação realizada ainda.").pack()
        return

    tree = ttk.Treeview(janela, columns=("valor", "juros", "parcelas", "tipo", "moeda", "parcela", "total", "juros_total"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col.capitalize())

    for item in historico:
        tree.insert("", tk.END, values=(
            item['valor'], item['juros'], item['parcelas'], item['tipo'], item['moeda'],
            f"{item['parcela']:.2f}", f"{item['total']:.2f}", f"{item['juros_total']:.2f}"
        ))
    tree.pack(expand=True, fill="both")

    botoes_frame = tk.Frame(janela)
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Exportar para CSV", command=salvar_historico_csv).pack(side="left", padx=5)
    tk.Button(botoes_frame, text="Exportar para JSON", command=salvar_historico_json).pack(side="left", padx=5)
    tk.Button(botoes_frame, text="Exibir Gráfico", command=lambda: exibir_grafico_embutido(janela)).pack(side="left", padx=5)
    tk.Button(botoes_frame, text="Sair", command=janela.destroy).pack(side="left", padx=5)

# Tela principal
def tela_principal():
    root = tk.Tk()
    root.title("Simulador de Financiamento Bancário")
    root.geometry("400x450")

    tk.Label(root, text="Simulador Bancário", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Simular Financiamento", width=30, command=tela_simulacao).pack(pady=5)
    tk.Button(root, text="Ver Histórico de Simulações", width=30, command=tela_historico).pack(pady=5)
    tk.Button(root, text="Alternar Modo Escuro", width=30, command=lambda: alternar_modo_escuro(root)).pack(pady=5)
    tk.Button(root, text="Jogar Adivinhação", width=30, command=iniciar_jogo).pack(pady=5)

    tutorial = (
        "Como usar:\n"
        "1. Escolha o valor do empréstimo.\n"
        "2. Ajuste a taxa de juros e número de parcelas.\n"
        "3. Selecione o tipo (PRICE ou SAC).\n"
        "4. Clique em 'Simular' para ver o resultado."
    )
    tk.Label(root, text=tutorial, wraplength=350, justify="left").pack(pady=10)
    tk.Button(root, text="Sair", width=30, command=root.quit).pack(pady=20)

    root.mainloop()

# Iniciar
if __name__ == "__main__":
    tela_principal()