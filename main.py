    import pandas as pd
    import numpy as np
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *

    # === ÁREA DE IMPORTAÇÃO E LEITURA ===
    df = pd.read_excel("RBC.xlsx")

    # Identificar colunas (remove ID/Caso e pega diagnóstico)
    atributos = [col for col in df.columns if col.lower() not in ['caso', 'id', 'diagnostico', 'diagnóstico']]
    diagnostico_col = [col for col in df.columns if 'diagn' in col.lower()]
    diagnostico_col = diagnostico_col[0] if len(diagnostico_col) > 0 else df.columns[-1]

    # === ÁREA DE DESIGN - JANELA PRINCIPAL ===
    app = ttk.Window("Diagnóstico de Artrite - RBC", themename="darkly")  # tema escuro
    app.geometry("1100x700")

    # Criar um Canvas para permitir rolagem vertical
    main_frame = ttk.Frame(app)
    main_frame.pack(fill=BOTH, expand=True)

    canvas = ttk.Canvas(main_frame)
    scroll_y = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    scroll_y.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Frame interno para os elementos
    container = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=container, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    container.bind("<Configure>", on_configure)

    # === ÁREA DE DESIGN - SEÇÕES ===
    frame_top = ttk.LabelFrame(container, text="🎚️ Definir Pesos (0.0 - 1.0)", padding=10, bootstyle="dark")
    frame_top.pack(fill=X, padx=10, pady=10)

    frame_middle = ttk.LabelFrame(container, text="🧍 Novo Caso - Entrada de Dados", padding=10, bootstyle="dark")
    frame_middle.pack(fill=X, padx=10, pady=10)

    frame_bottom = ttk.LabelFrame(container, text="📊 Resultados de Similaridade", padding=10, bootstyle="dark")
    frame_bottom.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # === ÁREA DE PESOS ===
    entradas_pesos = {}

    def validar_peso(event, nome):
        """Garante que o peso fique entre 0.0 e 1.0"""
        try:
            valor = float(entradas_pesos[nome].get())
            if valor < 0 or valor > 1:
                entradas_pesos[nome].delete(0, "end")
                entradas_pesos[nome].insert(0, "1.0")
        except ValueError:
            entradas_pesos[nome].delete(0, "end")
            entradas_pesos[nome].insert(0, "1.0")

    # Criação dos campos de peso
    for attr in atributos:
        row = ttk.Frame(frame_top)
        row.pack(fill=X, pady=3)
        ttk.Label(row, text=f"{attr}:", width=15).pack(side=LEFT)
        ent = ttk.Entry(row, width=10, bootstyle="dark")
        ent.insert(0, "1.0")
        ent.pack(side=LEFT)
        ent.bind("<FocusOut>", lambda e, nome=attr: validar_peso(e, nome))
        entradas_pesos[attr] = ent

    # === BOTÃO CALCULAR ===
    ttk.Label(container, text=" ").pack()  # espaçamento
    btn_calcular = ttk.Button(container, text="⚙️ Calcular Similaridade", bootstyle="success-outline")
    btn_calcular.pack(pady=10)

    # === ÁREA DE ENTRADA DO NOVO CASO ===
    entradas_valores = {}
    for attr in atributos:
        row = ttk.Frame(frame_middle)
        row.pack(fill=X, pady=3)
        ttk.Label(row, text=f"{attr}:", width=15).pack(side=LEFT)
        cb = ttk.Combobox(row, values=["Sim", "Não"], width=10, bootstyle="dark")
        cb.set("Sim")
        cb.pack(side=LEFT)
        entradas_valores[attr] = cb

    # === ÁREA DE RESULTADOS ===
    lbl_resultado = ttk.Label(container, text="", font=("Segoe UI", 14, "bold"), bootstyle="success")
    lbl_resultado.pack(pady=10)

    cols = ["Caso"] + atributos + [diagnostico_col, "Similaridade (%)"]
    tabela = ttk.Treeview(frame_bottom, columns=cols, show="headings", height=15)
    for col in cols:
        tabela.heading(col, text=col)
        tabela.column(col, anchor="center", width=85)
    tabela.pack(fill=BOTH, expand=True)

    scroll_table = ttk.Scrollbar(frame_bottom, orient="vertical", command=tabela.yview)
    tabela.configure(yscroll=scroll_table.set)
    scroll_table.pack(side=RIGHT, fill=Y)

    # === ÁREA DE LÓGICA RBC ===
    def calcular_rbc():
        """Calcula as similaridades com base nos pesos e entradas"""
        pesos = np.array([float(entradas_pesos[a].get()) for a in atributos])
        novo_caso = {a: entradas_valores[a].get().strip().lower() for a in atributos}

        similaridades = []
        for i, caso in df.iterrows():
            soma = 0
            for j, a in enumerate(atributos):
                valor_caso = str(caso[a]).strip().lower()
                if valor_caso == novo_caso[a]:
                    soma += pesos[j]
            total = np.sum(pesos)
            similaridade = (soma / total) * 100 if total > 0 else 0
            similaridades.append(similaridade)

        df_resultado = df.copy()
        df_resultado["Similaridade (%)"] = similaridades
        df_resultado["Caso"] = np.arange(1, len(df) + 1)
        df_resultado = df_resultado.sort_values(by="Similaridade (%)", ascending=False)

        for i in tabela.get_children():
            tabela.delete(i)
        for _, row in df_resultado.iterrows():
            valores = [row["Caso"]] + [row[a] for a in atributos] + [row[diagnostico_col], f"{row['Similaridade (%)']:.2f}"]
            tabela.insert("", "end", values=valores)

        top_case = df_resultado.iloc[0]
        lbl_resultado.config(
            text=f"🏆 Caso {int(top_case['Caso'])} é o mais similar ({top_case['Similaridade (%)']:.2f}%) → Diagnóstico provável: {top_case[diagnostico_col]}",
            bootstyle="success"
        )

    btn_calcular.config(command=calcular_rbc)

    # === FINALIZAÇÃO ===
    app.mainloop()
