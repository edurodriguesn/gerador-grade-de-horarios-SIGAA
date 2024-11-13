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
    dias_semana = range(2, 8)  # 2 = segunda-feira, 7 = sábado
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

# Função para exibir a grade usando Plotly com visualização ampliada
def exibir_grade_plotly(df_grade):
    df_grade = df_grade.T
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Horários/Dias"] + list(df_grade.columns),
            fill_color='paleturquoise',
            align='center',
            font=dict(size=14)
        ),
        cells=dict(
            values=[df_grade.index] + [df_grade[col].tolist() for col in df_grade.columns],
            fill_color='lavender',
            align='center',
            font=dict(size=12),
            height=30  # Aumenta a altura das células
        ))
    ])

    # Ajuste o tamanho da visualização
    fig.update_layout(
        width=1000,  # Largura da tabela
        height=600   # Altura da tabela
    )
    
    st.plotly_chart(fig, use_container_width=True)

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
    st.write("### Visualização da Grade de Horários")
    exibir_grade_plotly(df_grade)
