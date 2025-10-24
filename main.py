import pandas as pd
import numpy as np
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

df = pd.read_excel("RBC.xlsx", dtype=str)
df = df.map(lambda x: str(x).strip().lower() if pd.notnull(x) else "")

if "caso" in df.columns:
    id_col = "caso"
else:
    id_col = df.columns[0]
    print(f"Coluna 'caso' nao encontrada. Usando '{id_col}' como ID.")

df = df[df[id_col] != ""]
try:
    df[id_col] = df[id_col].astype(int)
except:
    print(f"Nao foi possivel converter '{id_col}' para inteiro. Mantendo como string.")

diagnostico_col = [c for c in df.columns if 'diagn' in c.lower()]
diagnostico_col = diagnostico_col[0] if diagnostico_col else df.columns[-1]
atributos = [c for c in df.columns if c.lower() not in [id_col.lower(), diagnostico_col.lower()]]

pesos_sugeridos = {
    'DL': 0.3, 'RC': 0.3, 'DC': 0.2, 'Mob': 0.4, 'DTS': 0.4,
    'IL': 0.7, 'ER': 0.9, 'TCSE': 0.7, 'ART': 0.8, 'RM': 0.6,
    'Bur': 0.4, 'Tof': 0.3, 'Sin': 0.5, 'ATG': 0.4, 'NR': 0.8,
    'HLA-B27': 0.4, 'DJ': 0.4
}

map_niveis = {
    'Mob': {'limitado':0, 'normal':1},
    'IL': {'ausente':0, 'leve':1, 'moderado':2, 'importante':3, 'muito_importante':4, 'importande':3, 'não':0},
    'ER': {'ausente':0, 'leve':1, 'moderado':2, 'importante':3, 'muito_importante':4, 'importande':3, 'não':0},
    'TCSE': {'não':0, 'moderado':1, 'importante':2, 'sim':3},
    'HLA-B27': {'não':0, '0':0, '0.5':1, '1':2}
}

# === Interface ===
app = ttk.Window("Diagnostico de Artrite - RBC", themename="darkly")
app.geometry("1350x860")

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

entradas_pesos = {}
for i, attr in enumerate(atributos):
    ttk.Label(inner_left, text=f"{attr}:").grid(row=i, column=0, sticky="w", padx=8, pady=4)
    ent = ttk.Entry(inner_left, width=8, bootstyle="dark")
    ent.insert(0, str(pesos_sugeridos.get(attr, 1.0)))
    ent.grid(row=i, column=1, padx=8, pady=4)
    entradas_pesos[attr] = ent

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

btn_calc = ttk.Button(main, text="Testar Diagnostico", bootstyle="success-outline")
btn_calc.grid(row=2, column=0, columnspan=2, pady=10)

btn_salvar = ttk.Button(main, text="Salvar Caso no Excel", bootstyle="info-outline")
btn_salvar.grid(row=3, column=0, columnspan=2, pady=10)

lbl_result = ttk.Label(main, text="", font=("Segoe UI", 14, "bold"), bootstyle="success")
lbl_result.grid(row=4, column=0, columnspan=2, pady=10)

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

def valor_num(attr, valor):
    valor = str(valor).strip().lower()
    if attr in map_niveis:
        return map_niveis[attr].get(valor, 0)
    return 1 if valor == "sim" else 0

def similaridade_local(attr, v1, v2):
    n1, n2 = valor_num(attr, v1), valor_num(attr, v2)
    if attr in map_niveis:
        max_val = max(map_niveis[attr].values())
        return 1 - (abs(n1 - n2) / max_val) if max_val > 0 else 0
    return 1 if n1 == n2 else 0

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

    for i in tabela.get_children():
        tabela.delete(i)
    for _, row in df_result.iterrows():
        vals = [row[id_col]] + [row[a] for a in atributos] + [row[diagnostico_col], f"{row['Similaridade (%)']:.2f}%"]
        tabela.insert("", "end", values=vals)

    top = df_result.iloc[0]
    lbl_result.config(
        text=f"Caso {top[id_col]} é o mais similar ({top['Similaridade (%)']:.2f}%) - Diagnóstico provável: {top[diagnostico_col]}"
    )

def salvar_caso():
    global df
    novo = {a: entradas_valores[a].get().strip().lower() for a in atributos}
    # verifica duplicado
    duplicado = df[atributos].apply(lambda row: all(row[a] == novo[a] for a in atributos), axis=1).any()
    if duplicado:
        messagebox.showwarning("Duplicado", "Já existe um caso com exatamente os mesmos atributos.")
        return
    try:
        novo_id = int(df[id_col].max()) + 1
    except:
        novo_id = len(df) + 1
    novo[diagnostico_col] = "novo"
    novo[id_col] = novo_id
    df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
    df.to_excel("RBC.xlsx", index=False)
    messagebox.showinfo("Salvo", f"Caso {novo_id} salvo com sucesso no RBC.xlsx!")

btn_calc.config(command=calcular_rbc)
btn_salvar.config(command=salvar_caso)

app.mainloop()
