import streamlit as st
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
    dias_semana = range(2, 8)
    horarios_tarde = {f'T{hr}': '' for hr in range(1, 6)}
    horarios_noite = {f'N{hr}': '' for hr in range(1, 6)}
    grade = {f"{dia}": {**horarios_tarde, **horarios_noite} for dia in dias_semana}
    horarios_ocupados = {f"{dia}": {f"T{hr}": "" for hr in range(1, 6)} | {f"N{hr}": "" for hr in range(1, 6)} for dia in dias_semana}
    conflitos = {}

    for disciplina, codigos in disciplinas.items():
        horarios_conflito = []
        conflito_detectado = False

        for codigo in codigos:
            dia, turno, horarios = interpretar_codigo(codigo)
            if dia in dias_semana:
                for horario in horarios:
                    chave_horario = f'{turno}{horario}'
                    if horarios_ocupados[str(dia)][chave_horario]:
                        disciplina_conflito = horarios_ocupados[str(dia)][chave_horario]
                        st.write(f"Conflito detectado! '{disciplina}' com '{disciplina_conflito}' no horário {dia} - {chave_horario}.")
                        horarios_conflito.append(chave_horario)
                        if disciplina_conflito not in conflitos:
                            conflitos[disciplina_conflito] = []
                        conflitos[disciplina_conflito].append(dia)
                        conflito_detectado = True

        if conflito_detectado:
            st.write(f"A disciplina '{disciplina}' foi removida devido ao conflito com outra.")
            continue

        for codigo in codigos:
            dia, turno, horarios = interpretar_codigo(codigo)
            if dia in dias_semana:
                for horario in horarios:
                    chave_horario = f'{turno}{horario}'
                    if chave_horario not in horarios_conflito:
                        horarios_ocupados[str(dia)][chave_horario] = disciplina

    df_grade = pd.DataFrame.from_dict(horarios_ocupados, orient='index')
    df_grade.index = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
    return df_grade

# Função para gerar a tabela como imagem
def gerar_imagem_tabela(df_grade):
    df_grade = df_grade.T
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Horários"] + list(df_grade.columns),
            fill_color='#2D3748',
            font=dict(color='white', size=16),  # Tamanho da fonte aumentado
            align='center'
        ),
        cells=dict(
            values=[df_grade.index] + [df_grade[col].tolist() for col in df_grade.columns],
            fill_color=[['#F7FAFC', '#E2E8F0'] * (len(df_grade.index) // 2)],
            font=dict(color='#2D3748', size=14),  # Tamanho da fonte aumentado
            align='center',
            height=50  # Aumento da altura das células
        ))
    ])

    # Ajustar o tamanho da figura para refletir maior proporção
    fig.update_layout(
        width=1000,  # Largura aumentada
        height=1100,  # Altura aumentada
        paper_bgcolor='white',  # Fundo branco para evitar interferência do tema do navegador
        plot_bgcolor='white',  # Fundo da área de plotagem também branco
        font=dict(color='#2D3748'),
        margin=dict(l=50, r=50, t=50, b=50),  # Aumentar as margens para dar mais espaço
    )

    # Salvar a imagem da tabela
    caminho_imagem = "tabela_grade_grande.png"
    fig.write_image(caminho_imagem)

    return caminho_imagem

# Função para ler as disciplinas a partir da entrada do usuário
def ler_disciplinas_entrada(entrada_texto):
    disciplinas = {}
    for linha in entrada_texto.splitlines():
        linha = linha.strip()
        if not linha:
            continue
        partes = linha.split(',')
        if len(partes) != 2:
            st.write(f"A linha '{linha}' não está no formato esperado.")
            continue
        nome_disciplina = partes[0].strip()
        codigos = partes[1].strip().split()
        if nome_disciplina not in disciplinas:
            disciplinas[nome_disciplina] = []
        disciplinas[nome_disciplina].extend(codigos)
    return disciplinas

# Configurar a interface do Streamlit
st.title("Grade de Horários - Visualizador de Disciplinas (by edurodriguesn)")

entrada_texto = st.text_area("Insira as disciplinas e horários no formato 'Disciplina, Código(s)':", height=200)
if st.button("Gerar Grade"):
    disciplinas = ler_disciplinas_entrada(entrada_texto)
    df_grade = organizar_grade(disciplinas)
    
    # Gerar a imagem da tabela
    imagem_tabela = gerar_imagem_tabela(df_grade)
    
    # Exibir a imagem da tabela
    st.image(imagem_tabela, caption="Grade de Horários", use_container_width=True)
