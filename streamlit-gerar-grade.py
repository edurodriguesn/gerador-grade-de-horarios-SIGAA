import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
import base64

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

# Função para gerar a tabela como base64
def gerar_imagem_tabela_base64(df_grade):
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
    fig.update_layout(
        width=1000,  # Largura aumentada
        height=1100,  # Altura aumentada
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color='#2D3748'),
        margin=dict(l=50, r=50, t=50, b=50)  # Aumentar as margens para dar mais espaço
    )
    # Gerar imagem em formato base64
    img_bytes = fig.to_image(format='png')  # Ajustar para usar a função to_image sem kaleido
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')  # Codificar a imagem para base64
    return f"data:image/png;base64,{img_base64}"

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
    
    # Gerar a imagem base64 da tabela
    imagem_tabela_base64 = gerar_imagem_tabela_base64(df_grade)
    
    # Exibir a imagem da tabela
    st.image(imagem_tabela_base64, caption="Grade de Horários", use_container_width=True)
    
    # Exibir conflitos de forma resumida abaixo da imagem
    if conflitos:
        st.write("Conflitos de horário detectados:")
        for disciplina, conflitos_disciplina in conflitos.items():
            st.write(f"Disciplina: {disciplina}")
            # Exibe uma mensagem simplificada com todos os conflitos
            st.write(f"  - Conflitos: {', '.join(conflitos_disciplina)}")
