import streamlit as st
import pandas as pd
import datetime
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# 1. CONFIGURAÇÕES INICIAIS
st.set_page_config(page_title="Conselho de Classe Imaculada", layout="wide", page_icon="📝")

# Configurar IA Gemini com sua chave dos Secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Erro: Verifique se a 'GOOGLE_API_KEY' está nos Secrets do Streamlit.")

# Configurar Acesso ao Google Drive usando as credenciais do GSheets
try:
    creds_info = st.secrets["connections"]["gsheets"]
    credentials = Credentials.from_service_account_info(creds_info, scopes=["https://www.googleapis.com/auth/drive"])
    drive_service = build('drive', 'v3', credentials=credentials)
except:
    st.error("Erro: Credenciais do Google Drive não encontradas nos Secrets.")

# Conexão com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
url_planilha = "https://docs.google.com/spreadsheets/d/1bGcDE5Q-Dz0dhQgeqcHiLSS8WUqc2icvWb4k8SwxAwQ/edit#gid=1477512121"

# --- CONFIGURAÇÃO DO DRIVE ---
# COLOQUE O ID DA SUA PASTA DO DRIVE ENTRE AS ASPAS ABAIXO:
PASTA_DESTINO_ID = "ID_DA_SUA_PASTA_AQUI"

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
        p1 = st.radio("1. O desempenho geral do aluno é:", ["Totalmente compatível", "Parcialmente compatível", "Abaixo do esperado", "Muito abaixo do esperado"], key="al1")
        p2 = st.radio("2. Evolução ao longo do período:", ["Significativa", "Gradual", "Pouca", "Não apresentou evolução"], key="al2")
        p3 = st.radio("3. Compreensão dos conteúdos essenciais:", ["Compreende plenamente", "Compreende com pequenas dificuldades", "Compreende parcialmente", "Apresenta grandes dificuldades"], key="al3")
        p4 = st.radio("4. O ritmo de aprendizagem do aluno é:", ["Adequado", "Um pouco abaixo", "Abaixo do esperado", "Muito abaixo"], key="al4")
        p5 = st.radio("5. O desempenho do aluno indica:", ["Domínio dos objetivos", "Atendimento parcial", "Atendimento mínimo", "Não atendimento"], key="al5")
        p6 = st.radio("6. A participação do aluno em sala é:", ["Frequente e ativa", "Regular", "Eventual", "Rara"], key="al6")
        p7 = st.radio("7. O interesse demonstrado pelo aluno é:", ["Elevado", "Moderado", "Baixo", "Muito baixo"], key="al7")
        p8 = st.radio("8. Quanto à atenção durante as aulas, o aluno:", ["Mantém atenção constante", "Pequenas dispersões", "Dispersa-se com frequência", "Raramente mantém atenção"], key="al8")
        p9 = st.radio("9. A autonomia do aluno na realização das atividades:", ["Alta", "Média", "Baixa", "Inexistente"], key="al9")
        p10 = st.radio("10. A postura do aluno no ambiente escolar é:", ["Adequada", "Parcialmente adequada", "Inadequada as vezes", "Frequentemente inadequada"], key="al10")
        p11 = st.radio("11. O aluno demonstra potencial nas áreas:", ["Linguagem e comunicação", "Raciocínio lógico/matemático", "Criatividade", "Ainda não apresenta destaque"], key="al11")
        p12 = st.radio("12. Em relação às orientações dos professores, o aluno:", ["Assimila e aplica", "Assimila parcialmente", "Dificuldade em aplicar", "Não demonstra assimilação"], key="al12")
        p13 = st.radio("13. O comprometimento com as atividades é:", ["Alto", "Moderado", "Baixo", "Muito baixo"], key="al13")
        p14 = st.radio("14. O aluno demonstra esforço mesmo diante de dificuldades?", ["Sempre", "Frequentemente", "Raramente", "Nunca"], key="al14")
        p15 = st.radio("15. O aluno apresenta:", ["Constância no desempenho", "Oscilações leves", "Oscilações frequentes", "Desempenho instável"], key="al15")
    with col_al2:
        p16 = st.radio("16. As dificuldades apresentadas pelo aluno são:", ["Pontuais", "Em alguns componentes", "Em vários componentes", "Generalizadas"], key="al16")
        p17 = st.radio("17. As principais dificuldades estão relacionadas a:", ["Conteúdo específico", "Interpretação e compreensão", "Organização e atenção", "Múltiplos fatores"], key="al17")
        p18 = st.radio("18. Nas avaliações, o aluno:", ["Demonstra domínio", "Demonstra compreensão parcial", "Demonstra insegurança", "Responde de forma aleatória"], key="al18")
        p19 = st.radio("19. Em relação à leitura e interpretação de enunciados:", ["Não apresenta dificuldades", "Apresenta pequenas dificuldades", "Dificuldades frequentes", "Grandes dificuldades"], key="al19")
        p20 = st.radio("20. O comportamento do aluno:", ["Não interfere no aprendizado", "Interfere ocasionalmente", "Interfere com frequência", "Compromete significativamente"], key="al20")
        p21 = st.radio("21. As dificuldades parecem estar relacionadas a:", ["Defasagem anterior", "Falta de estudo", "Concentração", "Conjunto de fatores"], key="al21")
        p22 = st.radio("22. O aluno responde melhor quando:", ["Trabalha autônomo", "Recebe mediação", "Trabalha em grupo", "Acompanhamento individual"], key="al22")
        p23 = st.radio("23. O acompanhamento familiar é:", ["Presente e efetivo", "Presente, porém irregular", "Pouco presente", "Inexistente"], key="al23")
        p24 = st.radio("24. O aluno demonstra consciência de suas dificuldades?", ["Sim, claramente", "Parcialmente", "Pouco", "Não demonstra"], key="al24")
        p25 = st.radio("25. O aluno utiliza estratégias próprias para aprender?", ["Sim, com autonomia", "Às vezes", "Raramente", "Não utiliza"], key="al25")
        p26 = st.radio("26. As estratégias pedagógicas adotadas até o momento:", ["Eficazes", "Parcialmente eficazes", "Pouco eficazes", "Sem efeito"], key="al26")
        p27 = st.radio("27. O aluno necessita de:", ["Acompanhamento regular", "Reforço pontual", "Reforço contínuo", "Acompanhamento individualizado"], key="al27")
        p28 = st.radio("28. A recuperação da aprendizagem deve ocorrer:", ["Em sala", "Atividades complementares", "Atendimento específico", "Múltiplas frentes"], key="al28")
        p29 = st.radio("29. Recomenda-se:", ["Manutenção atual", "Ajustes pontuais", "Reestruturação", "Plano individual"], key="al29")
        p30 = st.radio("30. Considerando o conjunto, o aluno apresenta:", ["Bom aproveitamento", "Aproveitamento parcial", "Baixo aproveitamento", "Intervenção intensiva"], key="al30")
    coment_aluno = st.text_area("💬 CONSIDERAÇÕES FINAIS (Individual):", key="cal")

# --- ABA 2: TURMA (20 PERGUNTAS) ---
with tab2:
    col_tr1, col_tr2 = st.columns(2)
    with col_tr1:
        t1 = st.radio("1. Desempenho geral da turma:", ["Muito satisfatório", "Satisfatório", "Parcialmente", "Insatisfatório"], key="t1")
        t2 = st.radio("2. Evolução letiva:", ["Significativa", "Gradual", "Pouca", "Nenhuma"], key="t2")
        t3 = st.radio("3. Compreensão de conteúdos essenciais?", ["Sim, plena", "Pequenas dificuldades", "Parcialmente", "Grandes dificuldades"], key="t3")
        t4 = st.radio("4. Ritmo de aprendizagem da turma:", ["Adequado", "Um pouco abaixo", "Abaixo", "Muito abaixo"], key="t4")
        t5 = st.radio("5. Participação nas atividades:", ["Ativa e constante", "Regular", "Irregular", "Baixa"], key="t5")
        t6 = st.radio("6. Interesse pelo aprendizado:", ["Elevado", "Moderado", "Baixo", "Muito baixo"], key="t6")
        t7 = st.radio("7. Atenção durante as aulas:", ["Constante", "Pequenas dispersões", "Dispersa com freq.", "Raramente mantém"], key="t7")
        t8 = st.radio("8. Autonomia da turma:", ["Alta", "Média", "Baixa", "Inexistente"], key="t8")
        t9 = st.radio("9. Postura geral da turma:", ["Adequada", "Parcialmente adequada", "Inadequada as vezes", "Frequentemente inadequada"], key="t9")
        t10 = st.radio("10. Cumprimento de tarefas e prazos:", ["Regular e pontual", "Majoritariamente regular", "Irregular", "Raramente cumprido"], key="t10")
    with col_tr2:
        t11 = st.radio("11. Organização de materiais:", ["Adequada", "Parcialmente", "Pouco adequada", "Inadequada"], key="t11")
        t12 = st.radio("12. Resultados das avaliações:", ["Bom domínio", "Domínio parcial", "Baixo domínio", "Insuficiente"], key="t12")
        t13 = st.radio("13. Dificuldades significativas em:", ["Pontuais", "Alguns componentes", "Vários componentes", "Generalizadas"], key="t13")
        t14 = st.radio("14. Leitura e interpretação:", ["Adequada", "Parcialmente adequada", "Deficiente", "Muito deficiente"], key="t14")
        t15 = st.radio("15. Desempenho no período:", ["Constante", "Pequenas oscilações", "Oscilações frequentes", "Instável"], key="t15")
        t16 = st.radio("16. Estratégias atenderam às necessidades?", ["Sim, plenamente", "Sim, parcialmente", "Pouco", "Não atenderam"], key="t16")
        t17 = st.radio("17. Responde melhor a:", ["Aulas expositivas", "Práticas/Dinâmicas", "Trabalhos em grupo", "Mediação constante"], key="t17")
        t18 = st.radio("18. Necessidade de replanejamento?", ["Não", "Ajustes pontuais", "Significativos", "Reestruturação total"], key="t18")
        t19 = st.radio("19. Recuperação necessária?", ["Não", "Pontuais", "Contínuas", "Intensivas"], key="t19")
        t20 = st.radio("20. Aproveitamento conjunto:", ["Bom", "Satisfatório", "Parcial", "Baixo"], key="t20")
    coment_turma = st.text_area("💬 CONSIDERAÇÕES FINAIS (Turma):", key="ctr")

# --- ABA 3: MATRÍCULAS ---
with tab3:
    st.subheader("📋 Relação de Alunos e Matrículas")
    try:
        df_mat = conn.read(spreadsheet=url_planilha, worksheet="Matriculas", ttl=0)
        busca = st.text_input("🔍 Buscar aluno pelo nome:", key="busca_mat")
        if busca:
            df_mat = df_mat[df_mat.iloc[:, 0].astype(str).str.contains(busca, case=False, na=False)]
        st.dataframe(df_mat, use_container_width=True, hide_index=True)
    except:
        st.info("Aba 'Matriculas' não encontrada.")

# --- BOTÃO DE PROCESSAMENTO FINAL ---
if st.button("🚀 FINALIZAR, SALVAR E GERAR RELATÓRIO", type="primary", use_container_width=True):
    if not prof or (not aluno_nome and not coment_turma):
        st.warning("Por favor, preencha a identificação e o nome do aluno/turma.")
    else:
        try:
            # 1. SALVAR NA PLANILHA
            dados = {
                "Data": datetime.datetime.now().strftime("%d/%m/%Y"), 
                "Prof": prof, "Turma": turma_sel, 
                "Aluno": aluno_nome if aluno_nome else "COLETIVO",
                "Conselho": coment_aluno if aluno_nome else coment_turma
            }
            df_atual = conn.read(spreadsheet=url_planilha, ttl=0)
            df_final = pd.concat([df_atual, pd.DataFrame([dados])], ignore_index=True)
            conn.update(spreadsheet=url_planilha, data=df_final)
            st.toast("✅ Dados salvos na planilha!")

            # 2. IA GEMINI (GERAR TEXTO)
            with st.spinner("🤖 A IA está redigindo o relatório pedagógico..."):
                if aluno_nome:
                    prompt = f"Como coordenador pedagógico, escreva um relatório descritivo para o aluno {aluno_nome}. Turma: {turma_sel}. Professor: {prof}. Baseie-se nestes pontos: Desempenho {p1}, Evolução {p2}, Participação {p6}, Interesse {p7}, Dificuldades {p16}. Comentário do prof: {coment_aluno}. Seja formal."
                else:
                    prompt = f"Escreva uma análise coletiva para a turma {turma_sel}. Desempenho {t1}, Interesse {t6}, Aproveitamento {t20}. Comentário: {coment_turma}."
                
                response = model.generate_content(prompt)
                texto_final = response.text

            # 3. GOOGLE DRIVE (CRIAR GOOGLE DOCS)
            file_metadata = {
                'name': f'Relatório {aluno_nome if aluno_nome else turma_sel} - {datetime.datetime.now().strftime("%d-%m")}',
                'parents': [PASTA_DESTINO_ID],
                'mimeType': 'application/vnd.google-apps.document'
            }
            
            # Cria o arquivo no Drive
            new_file = drive_service.files().create(body=file_metadata, fields='id, webViewLink').execute()
            
            st.success("🎉 Processo concluído com sucesso!")
            st.link_button("📂 Abrir Relatório no Google Docs", new_file.get('webViewLink'))
            
            st.markdown("---")
            st.subheader("📄 Prévia do Texto Gerado:")
            st.write(texto_final)

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
