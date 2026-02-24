import streamlit as st
import pandas as pd
import datetime
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Sistema Oficial de Conselho de Classe",
    layout="wide",
    page_icon="📝"
)

st.title("📝 Sistema Oficial de Conselho de Classe")

# =========================================================
# CONFIGURAÇÃO GEMINI
# =========================================================
@st.cache_resource
def configurar_ia():
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    return genai.GenerativeModel("gemini-1.5-flash")

# =========================================================
# CONFIGURAÇÃO GOOGLE DRIVE + DOCS
# =========================================================
@st.cache_resource
def configurar_google():
    creds_info = st.secrets["connections"]["gsheets"]

    credentials = Credentials.from_service_account_info(
        creds_info,
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/documents"
        ]
    )

    drive = build("drive", "v3", credentials=credentials)
    docs = build("docs", "v1", credentials=credentials)

    return drive, docs

model = configurar_ia()
drive_service, docs_service = configurar_google()
conn = st.connection("gsheets", type=GSheetsConnection)

# 🔴 CONFIGURE AQUI
url_planilha = "SUA_URL_DA_PLANILHA"
PASTA_DESTINO_ID = "SEU_ID_DA_PASTA_DRIVE"

# =========================================================
# IDENTIFICAÇÃO
# =========================================================
col1, col2 = st.columns(2)

with col1:
    professor = st.text_input("Nome do Professor(a)")

with col2:
    turma = st.selectbox(
        "Turma",
        ["1º Ano A", "2º Ano A", "3º Ano A", "4º Ano A", "5º Ano A"]
    )

tab1, tab2 = st.tabs(["Avaliação do Aluno", "Avaliação da Turma"])

# =========================================================
# AVALIAÇÃO DO ALUNO
# =========================================================
with tab1:
    aluno = st.text_input("Nome do Aluno")

    opcoes = ["Excelente", "Bom", "Regular", "Insatisfatório"]

    respostas_aluno = {}

    respostas_aluno["O desempenho geral do aluno é"] = st.selectbox("1. O desempenho geral do aluno é:", opcoes)
    respostas_aluno["Em relação à evolução ao longo do período, o aluno"] = st.selectbox("2. Em relação à evolução ao longo do período, o aluno:", ["Significativa", "Gradual", "Pouca", "Nenhuma"])
    respostas_aluno["Quanto à compreensão dos conteúdos essenciais, o aluno"] = st.selectbox("3. Quanto à compreensão dos conteúdos essenciais, o aluno:", opcoes)
    respostas_aluno["O ritmo de aprendizagem do aluno é"] = st.selectbox("4. O ritmo de aprendizagem do aluno é:", ["Rápido", "Adequado", "Lento"])
    respostas_aluno["A participação do aluno em sala é"] = st.selectbox("5. A participação do aluno em sala é:", opcoes)
    respostas_aluno["O interesse demonstrado pelo aluno é"] = st.selectbox("6. O interesse demonstrado pelo aluno é:", opcoes)
    respostas_aluno["Quanto à atenção durante as aulas, o aluno"] = st.selectbox("7. Quanto à atenção durante as aulas, o aluno:", opcoes)
    respostas_aluno["A autonomia na realização das atividades é"] = st.selectbox("8. A autonomia na realização das atividades é:", opcoes)
    respostas_aluno["A postura e comportamento são"] = st.selectbox("9. A postura e comportamento são:", ["Adequados", "Precisam melhorar"])
    respostas_aluno["A organização do aluno é"] = st.selectbox("10. A organização do aluno é:", opcoes)
    respostas_aluno["A responsabilidade com prazos é"] = st.selectbox("11. A responsabilidade com prazos é:", opcoes)
    respostas_aluno["O relacionamento com colegas é"] = st.selectbox("12. O relacionamento com colegas é:", opcoes)
    respostas_aluno["O relacionamento com o professor é"] = st.selectbox("13. O relacionamento com o professor é:", opcoes)
    respostas_aluno["A comunicação oral é"] = st.selectbox("14. A comunicação oral é:", opcoes)
    respostas_aluno["A produção escrita é"] = st.selectbox("15. A produção escrita é:", opcoes)
    respostas_aluno["A capacidade de interpretação é"] = st.selectbox("16. A capacidade de interpretação é:", opcoes)
    respostas_aluno["A resolução de problemas é"] = st.selectbox("17. A resolução de problemas é:", opcoes)
    respostas_aluno["O comprometimento com os estudos é"] = st.selectbox("18. O comprometimento com os estudos é:", opcoes)
    respostas_aluno["A frequência é"] = st.selectbox("19. A frequência é:", ["Excelente", "Boa", "Regular", "Baixa"])
    respostas_aluno["A pontualidade é"] = st.selectbox("20. A pontualidade é:", ["Sempre pontual", "Às vezes", "Frequentemente atrasado"])

    respostas_aluno["As principais dificuldades estão relacionadas a"] = st.selectbox(
        "21. As principais dificuldades estão relacionadas a:",
        ["Conteúdo específico", "Interpretação e compreensão", "Organização e atenção", "Defasagem anterior", "Múltiplos fatores", "Não apresenta dificuldades"]
    )

    respostas_aluno["Necessita acompanhamento pedagógico"] = st.selectbox("22. Necessita acompanhamento pedagógico?", ["Sim", "Não"])
    respostas_aluno["Necessita intervenção específica"] = st.selectbox("23. Necessita intervenção específica?", ["Sim", "Não"])
    respostas_aluno["Apresenta potencial de melhoria"] = st.selectbox("24. Apresenta potencial de melhoria?", ["Sim", "Não"])
    respostas_aluno["Demonstra protagonismo"] = st.selectbox("25. Demonstra protagonismo?", ["Sim", "Não"])
    respostas_aluno["Demonstra habilidades socioemocionais adequadas"] = st.selectbox("26. Demonstra habilidades socioemocionais adequadas?", ["Sim", "Não"])

    comentario_aluno = st.text_area("27. Considerações finais do professor")

# =========================================================
# AVALIAÇÃO DA TURMA
# =========================================================
with tab2:
    opcoes = ["Excelente", "Bom", "Regular", "Insatisfatório"]

    respostas_turma = {}

    respostas_turma["O desempenho geral da turma é"] = st.selectbox("1. O desempenho geral da turma é:", opcoes)
    respostas_turma["O nível de engajamento da turma é"] = st.selectbox("2. O nível de engajamento da turma é:", opcoes)
    respostas_turma["A disciplina coletiva é"] = st.selectbox("3. A disciplina coletiva é:", opcoes)
    respostas_turma["O rendimento acadêmico médio é"] = st.selectbox("4. O rendimento acadêmico médio é:", opcoes)
    respostas_turma["A participação nas aulas é"] = st.selectbox("5. A participação nas aulas é:", opcoes)
    respostas_turma["O interesse pelos conteúdos é"] = st.selectbox("6. O interesse pelos conteúdos é:", opcoes)
    respostas_turma["A organização coletiva é"] = st.selectbox("7. A organização coletiva é:", opcoes)
    respostas_turma["O cumprimento de prazos é"] = st.selectbox("8. O cumprimento de prazos é:", opcoes)
    respostas_turma["O relacionamento entre os alunos é"] = st.selectbox("9. O relacionamento entre os alunos é:", opcoes)
    respostas_turma["O respeito às normas institucionais é"] = st.selectbox("10. O respeito às normas institucionais é:", opcoes)
    respostas_turma["A maturidade da turma é"] = st.selectbox("11. A maturidade da turma é:", opcoes)
    respostas_turma["A colaboração entre colegas é"] = st.selectbox("12. A colaboração entre colegas é:", opcoes)
    respostas_turma["A evolução ao longo do período foi"] = st.selectbox("13. A evolução ao longo do período foi:", ["Significativa", "Gradual", "Pouca", "Nenhuma"])

    comentario_turma = st.text_area("14. Considerações gerais da turma")

# =========================================================
# GERAÇÃO DO RELATÓRIO
# =========================================================
if st.button("GERAR RELATÓRIO OFICIAL"):

    texto = ""

    if aluno:
        for pergunta, resposta in respostas_aluno.items():
            texto += f"{pergunta}: {resposta}\n"
        texto += f"\nConsiderações Finais: {comentario_aluno}"
    else:
        for pergunta, resposta in respostas_turma.items():
            texto += f"{pergunta}: {resposta}\n"
        texto += f"\nConsiderações Finais: {comentario_turma}"

    prompt = f"""
    Redija um relatório pedagógico institucional formal com base nas seguintes informações:

    Professor: {professor}
    Turma: {turma}
    Aluno: {aluno if aluno else "Relatório Geral da Turma"}

    Avaliações:
    {texto}

    Estruture em:
    - Análise Geral
    - Pontos Fortes
    - Pontos de Atenção
    - Recomendações Pedagógicas
    """

    response = model.generate_content(prompt)
    relatorio = response.text

    st.success("Relatório gerado com sucesso!")
    st.write(relatorio)
