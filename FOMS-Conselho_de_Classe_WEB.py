import streamlit as st
import pandas as pd
import datetime
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# 1. CONFIGURAÇÕES DA PÁGINA
st.set_page_config(page_title="Conselho de Classe Imaculada", layout="wide", page_icon="📝")

# --- FUNÇÕES DE CONEXÃO COM DEBUG AVANÇADO ---
@st.cache_resource
def configurar_ia():
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # LOGICA DE BUSCA AUTÔNOMA (ListModels)
        # Em vez de fixar um nome, vamos listar o que sua chave permite usar
        modelos_disponiveis = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                modelos_disponiveis.append(m.name)
        
        # Prioridade de escolha baseada na existência real na sua conta
        selecionado = None
        for alvo in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
            if alvo in modelos_disponiveis:
                selecionado = alvo
                break
        
        if selecionado:
            return genai.GenerativeModel(selecionado)
        else:
            st.error("Nenhum modelo compatível encontrado. Verifique se a Generative Language API está ativa no seu Google Cloud.")
            return None
            
    except Exception as e:
        st.error(f"Erro de Conexão/Autenticação: {e}")
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
        st.error(f"Erro Drive: {e}")
        return None

# Inicialização
model = configurar_ia()
drive_service = configurar_drive()
conn = st.connection("gsheets", type=GSheetsConnection)

# Configurações de destino
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

# --- ABA 1: ALUNO (30 PERGUNTAS) ---
with tab1:
    aluno_nome = st.text_input("🎓 Nome do Aluno")
    col_al1, col_al2 = st.columns(2)
    with col_al1:
        p1 = st.radio("1. Desempenho geral:", ["Totalmente compatível", "Parcialmente", "Abaixo", "Muito abaixo"], key="al1")
        p2 = st.radio("2. Evolução:", ["Significativa", "Gradual", "Pouca", "Nenhuma"], key="al2")
        p3 = st.radio("3. Conteúdos essenciais:", ["Plena", "Pequenas dificuldades", "Parcial", "Grandes dificuldades"], key="al3")
        p4 = st.radio("4. Ritmo de aprendizagem:", ["Adequado", "Um pouco abaixo", "Abaixo", "Muito abaixo"], key="al4")
        p5 = st.radio("5. Domínio dos objetivos:", ["Domina", "Parcial", "Mínimo", "Não atende"], key="al5")
        p6 = st.radio("6. Participação:", ["Frequente e ativa", "Regular", "Eventual", "Rara"], key="al6")
        p7 = st.radio("7. Interesse:", ["Elevado", "Moderado", "Baixo", "Muito baixo"], key="al7")
        p8 = st.radio("8. Atenção:", ["Constante", "Pequenas dispersões", "Frequente", "Rara"], key="al8")
        p9 = st.radio("9. Autonomia:", ["Alta", "Média", "Baixa", "Inexistente"], key="al9")
        p10 = st.radio("10. Postura escolar:", ["Adequada", "Parcialmente", "Inadequada as vezes", "Frequentemente inadequada"], key="al10")
        p11 = st.radio("11. Potencial:", ["Linguagem", "Lógica/Matemática", "Criatividade", "Sem destaque"], key="al11")
        p12 = st.radio("12. Orientações:", ["Assimila e aplica", "Assimila parcialmente", "Dificuldade", "Não assimila"], key="al12")
        p13 = st.radio("13. Comprometimento:", ["Alto", "Moderado", "Baixo", "Muito baixo"], key="al13")
        p14 = st.radio("14. Esforço:", ["Sempre", "Frequentemente", "Raramente", "Nunca"], key="al14")
        p15 = st.radio("15. Constância:", ["Constante", "Oscilações leves", "Frequentes", "Instável"], key="al15")
    with col_al2:
        p16 = st.radio("16. Dificuldades:", ["Pontuais", "Em alguns componentes", "Vários", "Generalizadas"], key="al16")
        p17 = st.radio("17. Causa dificuldades:", ["Conteúdo", "Interpretação", "Organização", "Múltiplos fatores"], key="al17")
        p18 = st.radio("18. Nas avaliações:", ["Domínio", "Compreensão parcial", "Insegurança", "Aleatório"], key="al18")
        p19 = st.radio("19. Leitura/Enunciados:", ["Sem dificuldades", "Pequenas", "Frequentes", "Grandes"], key="al19")
        p20 = st.radio("20. Comportamento interfere?", ["Não", "Ocasionalmente", "Com frequência", "Significativamente"], key="al20")
        p21 = st.radio("21. Relacionado a:", ["Defasagem", "Falta estudo", "Concentração", "Conjunto de fatores"], key="al21")
        p22 = st.radio("22. Responde melhor:", ["Autônomo", "Com mediação", "Em grupo", "Individual"], key="al22")
        p23 = st.radio("23. Família:", ["Presente", "Irregular", "Ausente", "Inexistente"], key="al23")
        p24 = st.radio("24. Consciência dificuldades:", ["Sim", "Parcial", "Pouco", "Não"], key="al24")
        p25 = st.radio("25. Estratégias próprias:", ["Sim", "Às vezes", "Raramente", "Não"], key="al25")
        p26 = st.radio("26. Pedagógico:", ["Eficazes", "Parciais", "Ineficazes", "Sem efeito"], key="al26")
        p27 = st.radio("27. Necessita de:", ["Regular", "Reforço", "Contínuo", "Individualizado"], key="al27")
        p28 = st.radio("28. Recuperação em:", ["Sala", "Extra", "Específico", "Múltiplos"], key="al28")
        p29 = st.radio("29. Recomenda-se:", ["Manutenção", "Ajustes", "Reestruturação", "Plano individual"], key="al29")
        p30 = st.radio("30. Aproveitamento:", ["Bom", "Parcial", "Baixo", "Intensivo"], key="al30")
    coment_aluno = st.text_area("💬 CONSIDERAÇÕES FINAIS (Individual):", key="cal")

# --- ABA 2: TURMA (20 PERGUNTAS) ---
with tab2:
    col_tr1, col_tr2 = st.columns(2)
    with col_tr1:
        t1 = st.radio("1. Desempenho turma:", ["Muito satisfatório", "Satisfatório", "Parcial", "Insatisfatório"], key="t1")
        t2 = st.radio("2. Evolução letiva:", ["Significativa", "Gradual", "Pouca", "Nenhuma"], key="t2")
        t3 = st.radio("3. Conteúdos:", ["Sim", "Dificuldades", "Parcial", "Grandes"], key="t3")
        t4 = st.radio("4. Ritmo:", ["Adequado", "Abaixo", "Muito abaixo"], key="t4")
        t5 = st.radio("5. Participação:", ["Ativa", "Regular", "Irregular", "Baixa"], key="t5")
        t6 = st.radio("6. Interesse:", ["Elevado", "Moderado", "Baixo"], key="t6")
        t7 = st.radio("7. Atenção:", ["Constante", "Dispersa", "Rara"], key="t7")
        t8 = st.radio("8. Autonomia:", ["Alta", "Média", "Baixa"], key="t8")
        t9 = st.radio("9. Postura:", ["Adequada", "Parcial", "Inadequada"], key="t9")
        t10 = st.radio("10. Prazos:", ["Regular", "Majoritariamente", "Raramente"], key="t10")
    with col_tr2:
        t11 = st.radio("11. Organização:", ["Adequada", "Parcial", "Inadequada"], key="t11")
        t12 = st.radio("12. Resultados:", ["Bons", "Parciais", "Baixos"], key="t12")
        t13 = st.radio("13. Dificuldades:", ["Pontuais", "Vários", "Generalizadas"], key="t13")
        t14 = st.radio("14. Leitura:", ["Adequada", "Deficiente", "Muito deficiente"], key="t14")
        t15 = st.radio("15. Desempenho Período:", ["Constante", "Oscilante", "Instável"], key="t15")
        t16 = st.radio("16. Estratégias Eficazes?", ["Sim", "Parcialmente", "Não"], key="t16")
        t17 = st.radio("17. Resposta a:", ["Expositivas", "Práticas", "Grupo"], key="t17")
        t18 = st.radio("18. Replanejamento:", ["Não", "Ajustes", "Total"], key="t18")
        t19 = st.radio("19. Recuperação:", ["Não", "Pontuais", "Intensivas"], key="t19")
        t20 = st.radio("20. Aproveitamento:", ["Bom", "Satisfatório", "Baixo"], key="t20")
    coment_turma = st.text_area("💬 CONSIDERAÇÕES FINAIS (Turma):", key="ctr")

# --- BOTÃO FINAL ---
if st.button("🚀 FINALIZAR E GERAR RELATÓRIO", type="primary", use_container_width=True):
    if not prof:
        st.warning("Preencha o nome do professor.")
    elif not model:
        st.error("IA não configurada. Verifique os segredos do Streamlit.")
    else:
        try:
            # 1. PLANILHA
            nova_linha = pd.DataFrame([{"Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), "Prof": prof, "Turma": turma_sel, "Aluno": aluno_nome if aluno_nome else "TURMA"}])
            df_atual = conn.read(spreadsheet=url_planilha, ttl=0)
            df_final = pd.concat([df_atual, nova_linha], ignore_index=True)
            conn.update(spreadsheet=url_planilha, data=df_final)
            
            # 2. IA
            with st.spinner("🤖 Gerando texto..."):
                prompt = f"Relatório Pedagógico Profissional. Professor: {prof}. Sujeito: {aluno_nome if aluno_nome else 'Turma '+turma_sel}. Dados: {p1 if aluno_nome else t1}. Observação: {coment_aluno if aluno_nome else coment_turma}."
                response = model.generate_content(prompt)
                texto_ia = response.text

            # 3. GOOGLE DOCS
            meta = {'name': f'Relatório {aluno_nome or turma_sel}', 'parents': [PASTA_DESTINO_ID], 'mimeType': 'application/vnd.google-apps.document'}
            res = drive_service.files().create(body=meta, fields='id, webViewLink').execute()
            
            st.success("🎉 Criado no Google Drive!")
            st.link_button("📂 Abrir no Google Docs", res.get('webViewLink'))
            st.write(texto_ia)
        except Exception as e:
            st.error(f"Erro: {e}")
