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
import plotly.graph_objects as go
import streamlit as st

import plotly.graph_objects as go
import streamlit as st

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
    fig.update_layout(width=1000, height=1100)
    st.plotly_chart(fig, use_container_width=True)


# Função para ler as disciplinas a partir da entrada do usuário
def ler_disciplinas_entrada(entrada_texto):
    disciplinas = {}
    # Dividir por quebras de linha e por "|"
    linhas = entrada_texto.splitlines()
    for linha in linhas:
        if not linha:
            continue
        # Aqui, vamos dividir pela barra "|" para obter cada disciplina
        partes = linha.split('|')
        for parte in partes:
            parte = parte.strip()
            if not parte:
                continue
            partes_disciplina = parte.split(',')
            if len(partes_disciplina) != 2:
                st.write(f"A linha '{parte}' não está no formato esperado.")
                continue
            nome_disciplina = partes_disciplina[0].strip()
            codigos = partes_disciplina[1].strip().split()
            if nome_disciplina not in disciplinas:
                disciplinas[nome_disciplina] = []
            disciplinas[nome_disciplina].extend(codigos)
    return disciplinas

# Opções predefinidas de disciplinas e horários com marcador de separação
opcoes_predefinidas = {
    "PROGRAMAÇÃO II": "2N5 3N12345|",
    "FÍSICA II": "4N1234|",
    "MATEMÁTICA DISCRETA": "2N1234|",
    "AUTÔMATOS E LINGUAGENS FORMAIS": "6N1234|",
    "METODOLOGIA DA PESQUISA E DO TRABALHO CIENTÍFICO": "6N1234|",
    "TEORIA DA COMPUTAÇÃO": "6T2345|",
    "TEORIA E PARADIGMAS DE LINGUAGENS DE PROGRAMAÇÃO": "2T2345|",
    "ARQUITETURA DE COMPUTADORES": "4T12345 7T5|",
    "ENGENHARIA DE SOFTWARE II": "2N12345 4N5|",
    "BANCO DE DADOS II": "5N12345 6N5|",
    "SISTEMAS OPERACIONAIS": "7N1234|",
    "REDES DE COMPUTADORES I": "4N2345|",
    "SISTEMAS DISTRIBUIDOS": "3N1234",
    "INTRODUÇÃO AO DIREITO": "4T1234",
    "COMPUTADOR SOCIEDADE E ÉTICA": "3T1234",
    "TÓPICOS EM ENGENHARIA DE SOFTWARE": "2T1234",
    "TÓPICOS EM COMPUTAÇÃO MÓVEL E SEM FIO": "6N1234",
    "CALCULO II": "6N12345 7N5",
    "EQUACOES DIFERENCIAIS E ORDINARIAS": "4T5 5T12345",
    "PROBABILIDADE E ESTATISTICA": "3T2345"

}

# Configurar a interface do Streamlit
st.title("Grade de Horários - Visualizador de Disciplinas (by edurodriguesn)")

# Campo de texto onde as disciplinas selecionadas são exibidas
entrada_texto = st.text_area("Insira as disciplinas e horários no formato 'Disciplina, Código(s)|':", height=200)

# Criar checkboxes para as opções predefinidas em colunas
disciplinas_selecionadas = []
num_colunas = 3  # Número de colunas para exibir as disciplinas lado a lado
cols = st.columns(num_colunas)

for i, (disciplina, codigo) in enumerate(opcoes_predefinidas.items()):
    coluna = cols[i % num_colunas]  # Distribuir em colunas
    with coluna:
        if st.checkbox(f"{disciplina}, {codigo}", key=f"{disciplina}-{codigo}"):
            linha_disciplina = f"{disciplina}, {codigo}"
            # Adiciona a disciplina em uma linha separada, removendo qualquer junção anterior
            if linha_disciplina not in entrada_texto.splitlines():
                entrada_texto += f"{linha_disciplina}\n"
            disciplinas_selecionadas.append(linha_disciplina)
        else:
            # Remove a disciplina do campo de texto se desmarcada
            entrada_texto = "\n".join(
                [linha for linha in entrada_texto.splitlines() if linha.strip() != f"{disciplina}, {codigo}"]
            ).strip()

# Limpar quebras de linha extras
entrada_texto = "\n".join(line for line in entrada_texto.splitlines() if line.strip())

# Adicionar separador '|' para cada linha no campo de texto ao final
entrada_texto = " | ".join(entrada_texto.splitlines())

# Botão para gerar a grade
if st.button("Gerar Grade"):
    disciplinas = ler_disciplinas_entrada(entrada_texto)
    df_grade, conflitos_unicos = organizar_grade(disciplinas)
    if conflitos_unicos:
        st.write("### Conflitos de Horários Detectados:")
        for conflito in conflitos_unicos:
            st.write(f"{conflito[0]} conflita com {conflito[1]}")
    st.write("### Visualização da Grade de Horários")
    exibir_grade_plotly(df_grade)

    # Exibir conflitos, se houver
   
