# Gerador de Grade de Horários Para Código do SIGAA

Caso deseje apenas acessar a funcionalidade, sem instalar, acesse o link <https://gerador-grade-de-horarios-sigaa.streamlit.app/>
## Pré-requisitos

Certifique-se de ter o seguinte instalado em seu sistema:

- Python 3.6 ou superior
- `pip` (gerenciador de pacotes do Python)

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/edurodriguesn/gerador-grade-de-horarios-SIGAA.git
```

### 2. Ao acessar, execute o script `env.sh` se estiver Linux

```bash
source env.sh
```

## 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

## Como Usar

### 1. Altere o arquivo `disciplinas.txt`

Coloque o nome da disciplina, seguido de vírgula(,) e em seguida o código do horário dela no SIGAA
Exemplo:

> PROGRAMAÇÃO II, 2N5 3T1234  
> FISICA II, 4N12345

Garanta que o seu arquivo `disciplinas.txt` estejam com esse formato, para que a aplicação funcione corretamente.


### 2. Executar o arquivo `grade_horarios.py`
```bash
python3 grade_horarios.py
```
<br><br><br>

## Sugestões de Melhorias no Código

Aqui estão algumas sugestões para melhorar o desempenho, legibilidade e uso da aplicação.

### 1. Alterar a identificação de horários

**Sugestão:** Trocar para o correspondente em horas. Atualmente o horário aparece como T1, T2, T2, etc... Mas seria bom aparecer como 13:30, 14:10, etc...

### 2. Reduzir a mensagem de informação de conflito de horário

**Sugestão:** Unificar os horários conflitantes em uma só mensagem ao invés de exibir cada horário que deu conflito.
