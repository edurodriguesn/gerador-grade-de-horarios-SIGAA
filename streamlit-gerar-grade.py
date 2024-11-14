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
    dias_semana = {2: "Segunda", 3: "Terça", 4: "Quarta", 5: "Quinta", 6: "Sexta", 7: "Sábado"}
    horarios_tarde = {f'T{hr}': '' for hr in range(1, 6)}
    horarios_noite = {f'N{hr}': '' for hr in range(1, 6)}
    grade = {f"{dia}": {**horarios_tarde, **horarios_noite} for dia in dias_semana}
    horarios_ocupados = {f"{dia}": {f"T{hr}": "" for hr in range(1, 6)} | {f"N{hr}": "" for hr in range(1, 6)} for dia in dias_semana}
    conflitos = []
    
    for disciplina, codigos in disciplinas.items():
        horarios_conflito = []

        for codigo in codigos:
            dia, turno, horarios = interpretar_codigo(codigo)
            if dia in dias_semana:
                for horario in horarios:
                    chave_horario = f'{turno}{horario}'
                    if horarios_ocupados[str(dia)][chave_horario]:
                        disciplina_conflito = horarios_ocupados[str(dia)][chave_horario]
                        conflitos.append(f"Conflito detectado! '{disciplina}' com '{disciplina_conflito}' na {dias_semana[dia]}, horário {chave_horario}.")
                        horarios_conflito.append(chave_horario)
                        
        if horarios_conflito:
            continue  # Pula a disciplina em conflito e não adiciona ao horário
            
        for codigo in codigos:
            dia, turno, horarios = interpretar_codigo(codigo)
            if dia in dias_semana:
                for horario in horarios:
                    chave_horario = f'{turno}{horario}'
                    if chave_horario not in horarios_conflito:
                        horarios_ocupados[str(dia)][chave_horario] = disciplina

    df_grade = pd.DataFrame.from_dict(horarios_ocupados, orient='index')
    df_grade.index = [dias_semana[int(dia)] for dia in horarios_ocupados.keys()]
    return df_grade, conflitos

# Função para exibir a grade usando Plotly com visualização ampliada
def exibir_grade_plotly(df_grade):
    df_grade = df_grade.T
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Horários/Dias"] + list(df_grade.columns),
            fill_color='white',  # Cor de fundo do cabeçalho
            font=dict(color='black', size=14),  # Cor do texto do cabeçalho
            align='center'
        ),
        cells=dict(
            values=[df_grade.index] + [df_grade[col].tolist() for col in df_grade.columns],
            fill_color='white',  # Cor de fundo das células
            font=dict(color='black', size=12),  # Cor do texto das células
            align='center',
            height=30
        ))
    ])

    # Ajuste o tamanho da visualização
    fig.update_layout(
        width=1000,  # Largura da tabela
        height=1100  # Altura da tabela
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
    st.write("### Visualização da Grade de Horários")
    exibir_grade_plotly(df_grade)

    if conflitos:
        st.write("### Conflitos de Horários Detectados:")
        for conflito in conflitos:
            st.write(conflito)
