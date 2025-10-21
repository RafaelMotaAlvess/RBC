import pandas as pd
import numpy as np
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# leitura e limpeza da base de dados
df = pd.read_excel("RBC.xlsx", dtype=str)

# usar map() em vez de applymap()
df = df.map(lambda x: str(x).strip().lower() if pd.notnull(x) else "")

# verifica se a coluna 'caso' existe, senao usa a primeira coluna
print("Colunas disponiveis:", df.columns.tolist())

if "caso" in df.columns:
    id_col = "caso"
else:
    id_col = df.columns[0]
    print(f"Coluna 'caso' nao encontrada. Usando '{id_col}' como ID.")

# remove linhas vazia e converte ID pra numero
df = df[df[id_col] != ""]
try:
    df[id_col] = df[id_col].astype(int)
except:
    print(f"Nao foi possivel converter '{id_col}' para inteiro. Mantendo como string.")

# detecta as colunas
diagnostico_col = [c for c in df.columns if 'diagn' in c.lower()]
diagnostico_col = diagnostico_col[0] if diagnostico_col else df.columns[-1]
atributos = [c for c in df.columns if c.lower() not in [id_col.lower(), diagnostico_col.lower()]]

print(f"ID: {id_col}")
print(f"Diagnostico: {diagnostico_col}")
print(f"Atributos: {atributos}")

# pesos sugerido para os atributos
pesos_sugeridos = {
    'DL': 0.7, 'RC': 0.8, 'DC': 0.9, 'Mob': 0.85, 'DTS': 0.6, 'IL': 0.95,
    'ER': 1.0, 'TCSE': 0.7, 'ART': 0.8, 'RM': 0.6, 'Bur': 0.5,
    'Tof': 0.5, 'Sin': 0.9, 'ATG': 0.7, 'NR': 0.8, 'HLA-B27': 0.7
}

# mapeamento de niveis para calculo
map_niveis = {
    'Mob': {'limitado':0, 'normal':1},
    'IL': {'ausente':0, 'leve':1, 'moderado':2, 'importante':3, 'muito_importante':4, 'importande':3, 'não':0},
    'ER': {'ausente':0, 'leve':1, 'moderado':2, 'importante':3, 'muito_importante':4, 'importande':3, 'não':0},
    'TCSE': {'não':0, 'moderado':1, 'importante':2, 'sim':3},
    'HLA-B27': {'não':0, '0':0, '0.5':1, '1':2}
}

# criação da interface grafica
app = ttk.Window("Diagnostico de Artrite - RBC", themename="darkly")
app.geometry("1350x820")

main = ttk.Frame(app, padding=15)
main.pack(fill=BOTH, expand=True)

frame_left = ttk.LabelFrame(main, text="Pesos dos Atributos", bootstyle="dark")
frame_right = ttk.LabelFrame(main, text="Novo Caso para Teste", bootstyle="dark")
frame_bottom = ttk.LabelFrame(main, text="Casos Ordenados por Similaridade", bootstyle="dark")

frame_left.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
frame_right.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
frame_bottom.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=8, pady=8)

main.columnconfigure(0, weight=1)
main.columnconfigure(1, weight=1)
main.rowconfigure(0, weight=2)
main.rowconfigure(1, weight=3)

# funcao pra adicionar scroll nas areas
def add_scroll(parent):
    canvas = ttk.Canvas(parent)
    scroll = ttk.Scrollbar(parent, orient=VERTICAL, command=canvas.yview)
    scroll.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    canvas.configure(yscrollcommand=scroll.set)
    inner = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=inner, anchor="nw")
    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    return inner

inner_left = add_scroll(frame_left)
inner_right = add_scroll(frame_right)

# campos para entrada dos pesos
entradas_pesos = {}
for i, attr in enumerate(atributos):
    ttk.Label(inner_left, text=f"{attr}:").grid(row=i, column=0, sticky="w", padx=8, pady=4)
    ent = ttk.Entry(inner_left, width=8, bootstyle="dark")
    ent.insert(0, str(pesos_sugeridos.get(attr, 1.0)))
    ent.grid(row=i, column=1, padx=8, pady=4)
    entradas_pesos[attr] = ent

# campos pra entrada do novo caso
entradas_valores = {}
for i, attr in enumerate(atributos):
    ttk.Label(inner_right, text=f"{attr}:").grid(row=i, column=0, sticky="w", padx=8, pady=4)
    if attr in map_niveis:
        cb = ttk.Combobox(inner_right, values=list(map_niveis[attr].keys()), width=18, bootstyle="dark")
        cb.set(list(map_niveis[attr].keys())[0])
    else:
        cb = ttk.Combobox(inner_right, values=["sim", "não"], width=18, bootstyle="dark")
        cb.set("não")
    cb.grid(row=i, column=1, padx=8, pady=4)
    entradas_valores[attr] = cb

# botao para executar o calculo
btn_calc = ttk.Button(main, text="Testar Diagnostico", bootstyle="success-outline")
btn_calc.grid(row=2, column=0, columnspan=2, pady=10)

lbl_result = ttk.Label(main, text="", font=("Segoe UI", 14, "bold"), bootstyle="success")
lbl_result.grid(row=3, column=0, columnspan=2, pady=10)

# tabela pra mostrar os resultados
cols = [id_col] + atributos + [diagnostico_col, "Similaridade (%)"]
tabela = ttk.Treeview(frame_bottom, columns=cols, show="headings", height=12)
for col in cols:
    tabela.heading(col, text=col)
    tabela.column(col, anchor="center", width=90)
tabela.pack(fill=BOTH, expand=True)

scroll_y = ttk.Scrollbar(frame_bottom, orient="vertical", command=tabela.yview)
scroll_x = ttk.Scrollbar(frame_bottom, orient="horizontal", command=tabela.xview)
tabela.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_x.pack(side=BOTTOM, fill=X)

# funcao que converte valor pra numero
def valor_num(attr, valor):
    valor = str(valor).strip().lower()
    if attr in map_niveis:
        return map_niveis[attr].get(valor, 0)
    return 1 if valor == "sim" else 0

# funcao pra calcular similaridade local entre dois valores
def similaridade_local(attr, v1, v2):
    n1, n2 = valor_num(attr, v1), valor_num(attr, v2)
    if attr in map_niveis:
        max_val = max(map_niveis[attr].values())
        return 1 - (abs(n1 - n2) / max_val) if max_val > 0 else 0
    return 1 if n1 == n2 else 0

# funcao principal que executa o RBC
def calcular_rbc():
    pesos = np.array([float(entradas_pesos[a].get()) for a in atributos])
    novo = {a: entradas_valores[a].get().strip().lower() for a in atributos}

    resultados = []
    for _, caso in df.iterrows():
        soma = sum(pesos[i] * similaridade_local(a, caso[a], novo[a]) for i, a in enumerate(atributos))
        total = np.sum(pesos)
        sim = (soma / total) * 100 if total > 0 else 0
        resultados.append(sim)

    df_result = df.copy()
    df_result["Similaridade (%)"] = np.round(resultados, 2)
    df_result = df_result.sort_values(by="Similaridade (%)", ascending=False).reset_index(drop=True)

    # limpa a tabela e mostra os casos ordenado
    for i in tabela.get_children():
        tabela.delete(i)
    for _, row in df_result.iterrows():
        vals = [row[id_col]] + [row[a] for a in atributos] + [row[diagnostico_col], f"{row['Similaridade (%)']:.2f}%"]
        tabela.insert("", "end", values=vals)

    # mostra o resultado principal
    top = df_result.iloc[0]
    try:
        caso_id = int(top[id_col])
    except:
        caso_id = top[id_col]
    
    lbl_result.config(
        text=f"Caso {caso_id} e o mais similar ({top['Similaridade (%)']:.2f}%) - Diagnostico provavel: {top[diagnostico_col]}"
    )

    # imprime no terminal
    print("\n===== RESULTADOS COMPLETOS (ordenados) =====")
    print(df_result[[id_col, "Similaridade (%)", diagnostico_col]].head(50))
    print(f"\nTotal de casos exibido: {len(df_result)}")

btn_calc.config(command=calcular_rbc)
app.mainloop()