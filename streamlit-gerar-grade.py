import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Função para interpretar o código da disciplina
def interpretar_codigo(codigo):
    dias = {
        2: 'Segunda-feira',
        3: 'Terça-feira',
        4: 'Quarta-feira',
        5: 'Quinta-feira',
        6: 'Sexta-feira',
        7: 'Sábado'
    }
    dia = int(codigo[0])
    turno = codigo[1]
    horarios = list(map(int, codigo[2:]))
    return dias[dia], turno, horarios

# Função para organizar a grade em um DataFrame, considerando conflitos de horários
def organizar_grade(disciplinas):
    dias_semana = range(2, 8)
    horarios_tarde = {f'T{hr}': '' for hr in range(1, 6)}
    horarios_noite = {f'N{hr}': '' for hr in range(1, 6)}
    grade = {f"{dia}": {**horarios_tarde, **horarios_noite} for dia in dias_semana}
    horarios_ocupados = {f"{dia}": {f"T{hr}": "" for hr in range(1, 6)} | {f"N{hr}": "" for hr in range(1, 6)} for dia in dias_semana}
    conflitos = {}

    for disciplina, codigos in disciplinas.items():
        conflitos_disciplina = []  # Lista para armazenar todos os conflitos dessa disciplina

        for codigo in codigos:
            dia, turno, horarios = interpretar_codigo(codigo)
            dia_numero = list(dias_semana)[list(dias_semana).index(int(codigo[0]))]
            if dia_numero in dias_semana:
                for horario in horarios:
                    chave_horario = f'{turno}{horario}'
                    if horarios_ocupados[str(dia_numero)][chave_horario]:
                        disciplina_conflito = horarios_ocupados[str(dia_numero)][chave_horario]
                        conflitos_disciplina.append(f"Conflito com '{disciplina_conflito}' no horário {dia} - {chave_horario}")

        if conflitos_disciplina:
            # Se houver conflitos, salva todos eles para essa disciplina
            conflitos[disciplina] = conflitos_disciplina
            continue  # Se houver conflito, essa disciplina será ignorada

        # Se não houver conflitos, preenche a grade com a disciplina
        for codigo in codigos:
            dia, turno, horarios = interpretar_codigo(codigo)
            dia_numero = list(dias_semana)[list(dias_semana).index(int(codigo[0]))]
            if dia_numero in dias_semana:
                for horario in horarios:
                    chave_horario = f'{turno}{horario}'
                    horarios_ocupados[str(dia_numero)][chave_horario] = disciplina

    df_grade = pd.DataFrame.from_dict(horarios_ocupados, orient='index')
    df_grade.index = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
    return df_grade, conflitos

# Função para gerar e exibir a tabela diretamente no Streamlit
# Função para gerar e exibir a tabela diretamente no Streamlit
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# CSS personalizado para expandir a largura
st.markdown(
    """
    <style>
        /* Aumenta a largura geral do conteúdo */
        .main .block-container {
            max-width: 90%;  /* Altera a largura máxima para 90% */
            padding: 1rem;  /* Ajusta o preenchimento */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Função para exibir a tabela como um gráfico no Streamlit
def exibir_tabela_grade(df_grade):
    df_grade = df_grade.T
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Horários"] + list(df_grade.columns),
            fill_color='#2D3748',
            font=dict(color='white', size=18),
            align='center'
        ),
        cells=dict(
            values=[df_grade.index] + [df_grade[col].tolist() for col in df_grade.columns],
            fill_color=[['#F7FAFC', '#E2E8F0'] * (len(df_grade.index) // 2)],
            font=dict(color='#2D3748', size=16),
            align='center',
            height=60
        ))
    ])
    fig.update_layout(
        width=1200,
        height=1000,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color='#2D3748'),
        margin=dict(l=20, r=20, t=20, b=20)
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
    df_grade, conflitos = organizar_grade(disciplinas)
    
    # Exibir a tabela da grade de horários
    exibir_tabela_grade(df_grade)
    
    # Exibir conflitos de forma resumida abaixo da tabela
    if conflitos:
        st.write("Conflitos de horário detectados:")
        for disciplina, conflitos_disciplina in conflitos.items():
            st.write(f"Disciplina: {disciplina}")
            st.write(f"  - Conflitos: {', '.join(conflitos_disciplina)}")
