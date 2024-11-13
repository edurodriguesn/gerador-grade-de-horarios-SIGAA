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
    # Definir apenas dias úteis de segunda a sábado
    dias_semana = range(2, 8)  # 2 = segunda-feira, 7 = sábado
    horarios_tarde = {f'T{hr}': '' for hr in range(1, 6)}
    horarios_noite = {f'N{hr}': '' for hr in range(1, 6)}
    grade = {f"{dia}": {**horarios_tarde, **horarios_noite} for dia in dias_semana}
    
    # Para armazenar quais horários já estão ocupados
    horarios_ocupados = {f"{dia}": {f"T{hr}": "" for hr in range(1, 6)} | {f"N{hr}": "" for hr in range(1, 6)} for dia in dias_semana}

    # Para manter controle dos conflitos
    conflitos = {}

    # Inserir disciplinas na estrutura, evitando conflitos de horários
    for disciplina, codigos in disciplinas.items():
        # Verificar conflitos antes de alocar
        horarios_conflito = []
        conflito_detectado = False  # Flag para identificar se houve um conflito

        for codigo in codigos:
            dia, turno, horarios = interpretar_codigo(codigo)
            if dia in dias_semana:
                for horario in horarios:
                    chave_horario = f'{turno}{horario}'
                    if horarios_ocupados[str(dia)][chave_horario]:
                        disciplina_conflito = horarios_ocupados[str(dia)][chave_horario]
                        print(f"Conflito detectado! A disciplina '{disciplina}' conflitante com '{disciplina_conflito}' no horário {dia} - {chave_horario}.")
                        # Marca o horário como ocupado pela disciplina em conflito
                        horarios_conflito.append(chave_horario)
                        if disciplina_conflito not in conflitos:
                            conflitos[disciplina_conflito] = []
                        conflitos[disciplina_conflito].append(dia)
                        conflito_detectado = True
        # Se houve conflito, a disciplina não será inserida na grade
        if conflito_detectado:
            print(f"A disciplina '{disciplina}' foi removida devido ao conflito com outra.")
            continue  # Pula a adição da disciplina em caso de conflito

        # Alocar a disciplina que não tem conflitos
        for codigo in codigos:
            dia, turno, horarios = interpretar_codigo(codigo)
            if dia in dias_semana:
                for horario in horarios:
                    chave_horario = f'{turno}{horario}'
                    if chave_horario not in horarios_conflito:
                        horarios_ocupados[str(dia)][chave_horario] = disciplina

    # Converter para DataFrame e mapear os dias
    df_grade = pd.DataFrame.from_dict(horarios_ocupados, orient='index')
    df_grade.index = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
    return df_grade

# Função para exibir a grade usando Plotly
def exibir_grade_plotly(df_grade):
    # Transpor o DataFrame para que os dias sejam as colunas e os horários as linhas
    df_grade = df_grade.T

    # Exibindo a grade com as células vazias (em branco) no lugar de 'null'
    fig = go.Figure(data=[go.Table(
        header=dict(values=["Horários/Dias"] + list(df_grade.columns),
                    fill_color='paleturquoise',
                    align='center'),
        cells=dict(values=[df_grade.index] + [df_grade[col].tolist() for col in df_grade.columns],
                   fill_color='lavender',
                   align='center'))
    ])
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
df_grade = organizar_grade(disciplinas)
exibir_grade_plotly(df_grade)
