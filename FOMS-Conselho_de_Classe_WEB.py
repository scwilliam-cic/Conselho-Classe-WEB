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
        # Modelo Pro para máxima compatibilidade e evitar erro 404
        return genai.GenerativeModel('models/gemini-1.5-pro')
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

# Conexão Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
url_planilha = "https://docs.google.com/spreadsheets/d/1bGcDE5Q-Dz0dhQgeqcHiLSS8WUqc2icvWb4k8SwxAwQ/edit#gid=1477512121"

# ID DA SUA PASTA
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
        p3 = st.radio("3. Compreensão conteúdos:", ["Plena", "Pequenas dificuldades", "Parcial", "Grandes dificuldades"], key="al3")
        p4 = st.radio("4. Ritmo de aprendizagem:", ["Adequado", "Um pouco abaixo", "Abaixo", "Muito abaixo"], key="al4")
        p5 = st.radio("5. Domínio dos objetivos:", ["Domina", "Parcial", "Mínimo", "Não atende"], key="al5")
        p6 = st.radio("6. Participação:", ["Ativa", "Regular", "Eventual", "Rara"], key="al6")
        p7 = st.radio("7. Interesse:", ["Elevado", "Moderado", "Baixo", "Muito baixo"], key="al7")
        p8 = st.radio("8. Atenção:", ["Constante", "Pequenas dispersões", "Frequente dispersão", "Rara atenção"], key="al8")
        p9 = st.radio("9. Autonomia:", ["Alta", "Média", "Baixa", "Inexistente"], key="al9")
        p10 = st.radio("10. Postura escolar:", ["Adequada", "Parcialmente", "Inadequada as vezes", "Sempre inadequada"], key="al10")
        p11 = st.radio("11. Potencial em:", ["Linguagem", "Lógica/Matemática", "Criatividade", "Sem destaque ainda"], key="al11")
        p12 = st.radio("12. Orientações prof:", ["Aplica", "Aplica parcialmente", "Dificuldade", "Não assimila"], key="al12")
        p13 = st.radio("13. Comprometimento:", ["Alto", "Moderado", "Baixo", "Muito baixo"], key="al13")
        p14 = st.radio("14. Esforço em dificuldades:", ["Sempre", "Frequentemente", "Raramente", "Nunca"], key="al14")
        p15 = st.radio("15. Constância:", ["Constante", "Oscilações leves", "Frequentes", "Instável"], key="al15")
    with col_al2:
        p16 = st.radio("16. Dificuldades são:", ["Pontuais", "Alguns componentes", "Vários", "Generalizadas"], key="al16")
        p17 = st.radio("17. Causa principal:", ["Conteúdo", "Interpretação", "Organização", "Múltiplos"], key="al17")
        p18 = st.radio("18. Nas avaliações:", ["Domina", "Compreende parcialmente", "Inseguro", "Aleatório"], key="al18")
        p19 = st.radio("19. Leitura/Enunciados:", ["Sem dificuldade", "Pequenas", "Frequentes", "Grandes"], key="al19")
        p20 = st.radio("20. Comportamento interfere?", ["Não", "Ocasionalmente", "Com frequência", "Significativamente"], key="al20")
        p21 = st.radio("21. Relacionado a:", ["Defasagem", "Falta estudo", "Concentração", "Fatores conjuntos"], key="al21")
        p22 = st.radio("22. Responde melhor:", ["Autônomo", "Com mediação", "Em grupo", "Individual"], key="al22")
        p23 = st.radio("23. Família:", ["Presente", "Irregular", "Pouco presente", "Inexistente"], key="al23")
        p24 = st.radio("24. Consciência dificuldades:", ["Sim", "Parcial", "Pouca", "Não"], key="al24")
        p25 = st.radio("25. Estratégias próprias:", ["Usa com autonomia", "Às vezes", "Raramente", "Não"], key="al25")
        p26 = st.radio("26. Estratégias pedagógicas:", ["Eficazes", "Parciais", "Pouco eficazes", "Sem efeito"], key="al26")
        p27 = st.radio("27. Necessita de:", ["Acomp. regular", "Reforço pontual", "Reforço contínuo", "Individualizado"], key="al27")
        p28 = st.radio("28. Recuperação em:", ["Sala", "Extra", "Atendimento específico", "Várias frentes"], key="al28")
        p29 = st.radio("29. Recomenda-se:", ["Manter", "Ajustes", "Reestruturar", "Plano individual"], key="al29")
        p30 = st.radio("30. Aproveitamento:", ["Bom", "Parcial", "Baixo", "Intervenção intensiva"], key="al30")
    coment_aluno = st.text_area("💬 CONSIDERAÇÕES FINAIS (Individual):", key="cal")

# --- ABA 2: TURMA (20 PERGUNTAS) ---
with tab2:
    col_tr1, col_tr2 = st.columns(2)
    with col_tr1:
        t1 = st.radio("1. Desempenho geral:", ["Satisfatório", "Parcial", "Insatisfatório"], key="t1")
        t2 = st.radio("2. Evolução:", ["Significativa", "Gradual", "Pouca"], key="t2")
        t3 = st.radio("3. Conteúdos essenciais:", ["Sim", "Dificuldades", "Não"], key="t3")
        t4 = st.radio("4. Ritmo:", ["Adequado", "Abaixo", "Muito abaixo"], key="t4")
        t5 = st.radio("5. Participação:", ["Ativa", "Regular", "Baixa"], key="t5")
        t6 = st.radio("6. Interesse:", ["Alto", "Médio", "Baixo"], key="t6")
        t7 = st.radio("7. Atenção:", ["Constante", "Dispersa", "Rara"], key="t7")
        t8 = st.radio("8. Autonomia:", ["Alta", "Média", "Baixa"], key="t8")
        t9 = st.radio("9. Postura:", ["Adequada", "Parcial", "Inadequada"], key="t9")
        t10 = st.radio("10. Prazos:", ["Regular", "Irregular", "Raramente"], key="t10")
    with col_tr2:
        t11 = st.radio("11. Organização:", ["Adequada", "Pouca", "Inadequada"], key="t11")
        t12 = st.radio("12. Resultados Avaliações:", ["Bons", "Médios", "Baixos"], key="t12")
        t13 = st.radio("13. Dificuldades:", ["Pontuais", "Vários", "Generalizadas"], key="t13")
        t14 = st.radio("14. Leitura:", ["Adequada", "Deficiente", "Muito deficiente"], key="t14")
        t15 = st.radio("15. Desempenho:", ["Constante", "Oscilante", "Instável"], key="t15")
        t16 = st.radio("16. Estratégias:", ["Eficazes", "Parciais", "Não atenderam"], key="t16")
        t17 = st.radio("17. Melhor resposta:", ["Expositivas", "Dinâmicas", "Grupo"], key="t17")
        t18 = st.radio("18. Replanejamento:", ["Não", "Ajustes", "Total"], key="t18")
        t19 = st.radio("19. Recuperação:", ["Não", "Pontual", "Intensiva"], key="t19")
        t20 = st.radio("20. Aproveitamento:", ["Bom", "Satisfatório", "Baixo"], key="t20")
    coment_turma = st.text_area("💬 CONSIDERAÇÕES FINAIS (Turma):", key="ctr")

# --- ABA 3: MATRÍCULAS ---
with tab3:
    try:
        df_mat = conn.read(spreadsheet=url_planilha, worksheet="Matriculas", ttl=0)
        st.dataframe(df_mat, use_container_width=True, hide_index=True)
    except:
        st.info("Aguardando carregamento da aba 'Matriculas'...")

# --- BOTÃO FINAL ---
if st.button("🚀 FINALIZAR E GERAR RELATÓRIO", type="primary", use_container_width=True):
    if not prof:
        st.warning("Por favor, preencha o nome do professor.")
    elif not model or not drive_service:
        st.error("Os serviços de IA ou Drive não carregaram. Verifique os Secrets.")
    else:
        try:
            # 1. SALVAR NO SHEETS
            nova_linha = pd.DataFrame([{"Data": datetime.datetime.now().strftime("%d/%m/%Y"), "Prof": prof, "Turma": turma_sel, "Aluno": aluno_nome if aluno_nome else "TURMA"}])
            df_atual = conn.read(spreadsheet=url_planilha, ttl=0)
            df_final = pd.concat([df_atual, nova_linha], ignore_index=True)
            conn.update(spreadsheet=url_planilha, data=df_final)
            st.toast("✅ Planilha atualizada!")

            # 2. GERAR TEXTO COM IA
            with st.spinner("🤖 IA redigindo relatório..."):
                if aluno_nome:
                    prompt = f"Escreva um relatório pedagógico formal para o aluno {aluno_nome}. Turma: {turma_sel}. Desempenho: {p1}. Participação: {p6}. Dificuldade: {p16}. Recomendação: {p29}. Comentário do prof: {coment_aluno}."
                else:
                    prompt = f"Escreva uma análise coletiva para a turma {turma_sel}. Aproveitamento: {t20}. Interesse: {t6}. Comentário: {coment_turma}."
                
                response = model.generate_content(prompt)
                texto_ia = response.text

            # 3. CRIAR GOOGLE DOCS NO DRIVE
            file_metadata = {
                'name': f'Relatório {aluno_nome if aluno_nome else turma_sel} - {datetime.datetime.now().strftime("%d-%m")}',
                'parents': [PASTA_DESTINO_ID],
                'mimeType': 'application/vnd.google-apps.document'
            }
            res = drive_service.files().create(body=file_metadata, fields='id, webViewLink').execute()
            
            st.success("🎉 Concluído! O arquivo foi criado na sua pasta do Drive.")
            st.link_button("📂 Abrir no Google Docs", res.get('webViewLink'))
            st.markdown("### Prévia do Texto Gerado:")
            st.write(texto_ia)

        except Exception as e:
            st.error(f"Erro no processamento: {e}")
