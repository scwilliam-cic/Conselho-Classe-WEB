import streamlit as st
import pandas as pd
import datetime
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# 1. CONFIGURAÇÕES DA PÁGINA
st.set_page_config(page_title="Conselho de Classe Imaculada", layout="wide", page_icon="📝")

# --- FUNÇÕES DE CONEXÃO ---
@st.cache_resource
def configurar_ia():
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        # USANDO O MODELO 1.0 PRO PARA EVITAR ERRO 404 DE VERSÃO BETA
        return genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Erro ao configurar IA: {e}")
        return None

@st.cache_resource
def configurar_drive():
    try:
        creds_info = st.secrets["connections"]["gsheets"]
        credentials = Credentials.from_service_account_info(
            creds_info, 
            scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/documents"]
        )
        return build('drive', 'v3', credentials=credentials)
    except Exception as e:
        st.error(f"Erro ao configurar Google Drive: {e}")
        return None

# Inicializa serviços
model = configurar_ia()
drive_service = configurar_drive()
conn = st.connection("gsheets", type=GSheetsConnection)

url_planilha = "https://docs.google.com/spreadsheets/d/1bGcDE5Q-Dz0dhQgeqcHiLSS8WUqc2icvWb4k8SwxAwQ/edit#gid=1477512121"
PASTA_DESTINO_ID = "1ZGdFybd_aPQZyvuPuitVB-JpZKc_nZP-"

st.title("📝 Formulário de Conselho de Classe")

# --- IDENTIFICAÇÃO ---
c1, c2 = st.columns(2)
with c1: 
    prof = st.text_input("👤 Nome do Professor(a)")
with c2: 
    turma_sel = st.selectbox("🏫 Turma", ["1º Ano A", "2º Ano A", "3º Ano A", "4º Ano A", "5º Ano A"])

tab1, tab2, tab3 = st.tabs(["🎓 Avaliação Aluno", "👥 Avaliação Turma", "📋 Consulta de Matrículas"])

# --- ABA 1: ALUNO (TODAS AS 30 PERGUNTAS) ---
with tab1:
    aluno_nome = st.text_input("🎓 Nome do Aluno")
    col_al1, col_al2 = st.columns(2)
    with col_al1:
        p1 = st.radio("1. Desempenho geral:", ["Totalmente compatível", "Parcialmente", "Abaixo", "Muito abaixo"], key="al1")
        p2 = st.radio("2. Evolução:", ["Significativa", "Gradual", "Pouca", "Nenhuma"], key="al2")
        p3 = st.radio("3. Conteúdos essenciais:", ["Plena", "Pequenas dificuldades", "Parcial", "Grandes dificuldades"], key="al3")
        p4 = st.radio("4. Ritmo:", ["Adequado", "Abaixo", "Muito abaixo"], key="al4")
        p5 = st.radio("5. Objetivos:", ["Domina", "Parcial", "Mínimo", "Não atende"], key="al5")
        p6 = st.radio("6. Participação:", ["Ativa", "Regular", "Rara"], key="al6")
        p7 = st.radio("7. Interesse:", ["Elevado", "Moderado", "Baixo"], key="al7")
        p8 = st.radio("8. Atenção:", ["Constante", "Dispersa", "Rara"], key="al8")
        p9 = st.radio("9. Autonomia:", ["Alta", "Média", "Baixa"], key="al9")
        p10 = st.radio("10. Postura:", ["Adequada", "Parcial", "Inadequada"], key="al10")
        p11 = st.radio("11. Potencial:", ["Linguagem", "Lógica", "Criatividade", "Nenhum"], key="al11")
        p12 = st.radio("12. Orientações:", ["Aplica", "Parcial", "Não aplica"], key="al12")
        p13 = st.radio("13. Comprometimento:", ["Alto", "Médio", "Baixo"], key="al13")
        p14 = st.radio("14. Esforço:", ["Sempre", "Às vezes", "Nunca"], key="al14")
        p15 = st.radio("15. Constância:", ["Constante", "Oscilante", "Instável"], key="al15")
    with col_al2:
        p16 = st.radio("16. Dificuldades:", ["Pontuais", "Algumas", "Muitas", "Geral"], key="al16")
        p17 = st.radio("17. Causa:", ["Conteúdo", "Interpretação", "Organização", "Outros"], key="al17")
        p18 = st.radio("18. Avaliações:", ["Bom domínio", "Parcial", "Inseguro"], key="al18")
        p19 = st.radio("19. Leitura:", ["Sem dificuldade", "Pequenas", "Grandes"], key="al19")
        p20 = st.radio("20. Comportamento interfere?", ["Não", "Às vezes", "Sim"], key="al20")
        p21 = st.radio("21. Motivo dificuldade:", ["Defasagem", "Falta estudo", "Concentração"], key="al21")
        p22 = st.radio("22. Responde melhor:", ["Sozinho", "Com ajuda", "Em grupo"], key="al22")
        p23 = st.radio("23. Família:", ["Presente", "Irregular", "Ausente"], key="al23")
        p24 = st.radio("24. Consciência:", ["Sim", "Pouca", "Não"], key="al24")
        p25 = st.radio("25. Estratégias:", ["Usa", "Às vezes", "Não"], key="al25")
        p26 = st.radio("26. Pedagógico:", ["Eficaz", "Parcial", "Ineficaz"], key="al26")
        p27 = st.radio("27. Necessita:", ["Regular", "Reforço", "Individual"], key="al27")
        p28 = st.radio("28. Recuperação:", ["Sala", "Extra", "Específica"], key="al28")
        p29 = st.radio("29. Recomenda:", ["Manter", "Ajustar", "Plano novo"], key="al29")
        p30 = st.radio("30. Aproveitamento:", ["Bom", "Regular", "Baixo"], key="al30")
    coment_aluno = st.text_area("💬 CONSIDERAÇÕES FINAIS (Individual):", key="cal")

# --- ABA 2: TURMA (TODAS AS 20 PERGUNTAS) ---
with tab2:
    col_tr1, col_tr2 = st.columns(2)
    with col_tr1:
        for i in range(1, 11): st.radio(f"{i}. Pergunta Turma {i}:", ["Bom", "Regular", "Baixo"], key=f"t{i}")
    with col_tr2:
        for i in range(11, 21): st.radio(f"{i}. Pergunta Turma {i}:", ["Bom", "Regular", "Baixo"], key=f"t{i}")
    coment_turma = st.text_area("💬 CONSIDERAÇÕES FINAIS (Turma):", key="ctr")

# --- ABA 3: MATRÍCULAS ---
with tab3:
    try:
        df_mat = conn.read(spreadsheet=url_planilha, worksheet="Matriculas", ttl=0)
        st.dataframe(df_mat, use_container_width=True, hide_index=True)
    except: st.info("Carregando matrículas...")

# --- BOTÃO FINAL ---
if st.button("🚀 FINALIZAR E GERAR RELATÓRIO", type="primary", use_container_width=True):
    if not prof: st.warning("Nome do professor é obrigatório.")
    elif not model: st.error("IA não disponível. Verifique a sua GOOGLE_API_KEY.")
    else:
        try:
            # 1. SALVAR NO SHEETS
            nova_linha = pd.DataFrame([{"Data": datetime.datetime.now().strftime("%d/%m/%Y"), "Prof": prof, "Turma": turma_sel, "Aluno": aluno_nome if aluno_nome else "TURMA"}])
            df_atual = conn.read(spreadsheet=url_planilha, ttl=0)
            df_final = pd.concat([df_atual, nova_linha], ignore_index=True)
            conn.update(spreadsheet=url_planilha, data=df_final)
            
            # 2. IA
            with st.spinner("🤖 Redigindo relatório pedagógico..."):
                prompt = f"Escreva um relatório para o aluno {aluno_nome}. Desempenho: {p1}. Comentário: {coment_aluno}. Seja formal."
                response = model.generate_content(prompt)
                texto_ia = response.text

            # 3. DRIVE
            file_metadata = {'name': f'Relatório {aluno_nome or turma_sel}', 'parents': [PASTA_DESTINO_ID], 'mimeType': 'application/vnd.google-apps.document'}
            res = drive_service.files().create(body=file_metadata, fields='id, webViewLink').execute()
            
            st.success("🎉 Sucesso! Relatório salvo no Google Drive.")
            st.link_button("📂 Abrir no Google Docs", res.get('webViewLink'))
            st.write(texto_ia)
        except Exception as e: st.error(f"Erro: {e}")
