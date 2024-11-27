import pandas as pd
import plotly.graph_objects as go

# Função para interpretar o código da disciplina
def interpretar_codigo(codigo):
    dia = int(codigo[0])
    turno = codigo[1]
    horarios = list(map(int, codigo[2:]))
    return dia, turno, horarios

# Função para organizar a grade em um DataFrame, considerando conflitos de horários
def organizar_grade(disciplinas):
    dias_semana = {2: "Segunda", 3: "Terça", 4: "Quarta", 5: "Quinta", 6: "Sexta", 7: "Sábado"}
    horarios_tarde = {f'T{hr}': '' for hr in range(1, 6)}
    horarios_noite = {f'N{hr}': '' for hr in range(1, 6)}
    grade = {f"{dia}": {**horarios_tarde, **horarios_noite} for dia in dias_semana}
    horarios_ocupados = {f"{dia}": {f"T{hr}": "" for hr in range(1, 6)} | {f"N{hr}": "" for hr in range(1, 6)} for dia in dias_semana}
    
    conflitos_unicos = set()
    
    for disciplina, codigos in disciplinas.items():
        horarios_conflito = []
        
        for codigo in codigos:
            dia, turno, horarios = interpretar_codigo(codigo)
            if dia in dias_semana:
                for horario in horarios:
                    chave_horario = f'{turno}{horario}'
                    disciplina_conflito = horarios_ocupados[str(dia)].get(chave_horario)
                    if disciplina_conflito:
                        conflito = tuple(sorted([disciplina, disciplina_conflito]))
                        conflitos_unicos.add(conflito)
                        horarios_conflito.append(chave_horario)
        
        if horarios_conflito:
            continue
        
        for codigo in codigos:
            dia, turno, horarios = interpretar_codigo(codigo)
            if dia in dias_semana:
                for horario in horarios:
                    chave_horario = f'{turno}{horario}'
                    if chave_horario not in horarios_conflito:
                        horarios_ocupados[str(dia)][chave_horario] = disciplina

    df_grade = pd.DataFrame.from_dict(horarios_ocupados, orient='index')
    df_grade.index = [dias_semana[int(dia)] for dia in horarios_ocupados.keys()]
    return df_grade, conflitos_unicos

# Função para exibir a grade usando Plotly com visualização ampliada
def exibir_grade_plotly(df_grade):
    horarios_map = {
        'T1': '13:30', 'T2': '14:20', 'T3': '15:10', 'T4': '16:20', 'T5': '17:10',
        'N1': '18:10', 'N2': '19:00', 'N3': '19:50', 'N4': '21:00', 'N5': '21:50'
    }
    df_grade = df_grade.rename(columns=horarios_map)
    df_grade = df_grade.T
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Horários"] + list(df_grade.columns),
            fill_color='white',
            font=dict(color='black', size=14),
            align='center',
            line_color='black'  # Define a cor preta para as bordas do cabeçalho
        ),
        cells=dict(
            values=[df_grade.index] + [df_grade[col].tolist() for col in df_grade.columns],
            fill_color='white',
            font=dict(color='black', size=12),
            align='center',
            height=30,
            line_color='black'  # Define a cor preta para as bordas das células
        ))
    ])
    
    # Atualizar layout para o gráfico
    fig.show()

# Função para ler o arquivo de disciplinas
def ler_disciplinas(arquivo):
    disciplinas = {}
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()  # Remove espaços em branco ao redor da linha
            if not linha:  # Ignora linhas vazias
                continue
            partes = linha.split(',')  # Divide nome e código usando a vírgula
            if len(partes) != 2:  # Se a linha não tiver exatamente 2 partes, ignora
                print(f"A linha '{linha}' não está no formato esperado.")
                continue
            nome_disciplina = partes[0].strip()  # O nome da disciplina
            codigos = partes[1].strip().split()  # Os códigos vêm após a vírgula
            if nome_disciplina not in disciplinas:
                disciplinas[nome_disciplina] = []
            disciplinas[nome_disciplina].extend(codigos)
    return disciplinas

# Ler as disciplinas do arquivo
disciplinas = ler_disciplinas("disciplinas.txt")

# Organizar e exibir a grade
df_grade, conflitos = organizar_grade(disciplinas)
print("Grade de Horários:")
print(df_grade)

if conflitos:
    print("\nConflitos de Horários Encontrados:")
    for conflito in conflitos:
        print(f"Conflito entre: {conflito[0]} e {conflito[1]}")

# Exibir a grade em um gráfico interativo
exibir_grade_plotly(df_grade)
