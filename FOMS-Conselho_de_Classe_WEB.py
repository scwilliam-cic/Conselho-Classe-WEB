import streamlit as st
import pandas as pd
import datetime
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection
from googleapiclient.discovery import build
from google.oauth2 import service_account

# 1. CONFIGURAÇÕES INICIAIS
st.set_page_config(page_title="Conselho de Classe Inteligente v3", layout="wide", page_icon="🎓")

# Chave Gemini Atualizada
GEMINI_KEY = "AIzaSyBKgQX3Ov1_1bB3BPBsRhKR1mi7CSd7TVI"
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# Conexão GSheets
conn = st.connection("gsheets", type=GSheetsConnection)
url_planilha = "https://docs.google.com/spreadsheets/d/1bGcDE5Q-Dz0dhQgeqcHiLSS8WUqc2icvWb4k8SwxAwQ/edit#gid=1477512121"

# --- FUNÇÃO: REDAÇÃO INTELIGENTE (GEMINI) ---
def redigir_relatorio_ia(dados):
    prompt = f"""
    Você é um psicopedagogo altamente qualificado. Sua tarefa é redigir um relatório de conselho de classe 
    profissional, empático e detalhado para o aluno {dados['Aluno']}.
    
    DADOS COLETADOS:
    - Professor: {dados['Prof']} | Turma: {dados['Turma']}
    - Desempenho Acadêmico: {dados['p1']} | Evolução: {dados['p2']} | Compreensão: {dados['p3']}
    - Ritmo de Aprendizado: {dados['p4']} | Atenção: {dados['p8']} | Autonomia: {dados['p9']}
    - Comportamento/Postura: {dados['p10']} e {dados['p20']}
    - Dificuldades Específicas: {dados['p16']} focadas em {dados['p17']}
    - Acompanhamento Familiar: {dados['p23']}
    - Comentário Livre do Professor: {dados['comentario']}

    DIRETRIZES DO TEXTO:
    1. Não use tópicos ou listas. Escreva de 3 a 4 parágrafos fluídos.
    2. Utilize termos técnicos pedagógicos (ex: defasagem, mediação, desenvolvimento socioemocional).
    3. O texto deve ser único e ter personalidade, variando a estrutura conforme as respostas.
    4. Termine com uma sugestão de intervenção pedagógica baseada nas dificuldades citadas.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao gerar texto com IA: {e}"

# --- FUNÇÃO: CRIAÇÃO DO GOOGLE DOC ---
def gerar_google_doc(nome_aluno, turma, texto_ia):
    # Puxa credenciais dos Secrets do Streamlit (as mesmas que você já usa para o Sheets)
    creds_info = st.secrets["connections.gsheets"]
    creds = service_account.Credentials.from_service_account_info(creds_info)
    
    docs_service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # Cria o arquivo no Drive
    doc_metadata = {'title': f'Relatório Pedagógico - {nome_aluno} ({turma}) - {datetime.datetime.now().year}'}
    doc = docs_service.documents().create(body=doc_metadata).execute()
    doc_id = doc.get('documentId')

    # Insere o conteúdo gerado pela IA
    requests = [{'insertText': {'location': {'index': 1}, 'text': texto_ia}}]
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    
    return f"https://docs.google.com/document/d/{doc_id}/edit"

# --- INTERFACE ---
st.title("📝 Formulário de Conselho de Classe com IA")

# Identificação
c1, c2 = st.columns(2)
with c1: prof = st.text_input("👤 Nome do Professor(a)")
with c2: turma_sel = st.selectbox("🏫 Turma", ["1º Ano A", "2º Ano A", "3º Ano A", "4º Ano A", "5º Ano A"])

tab1, tab2, tab3 = st.tabs(["🎓 Avaliação Individual", "👥 Avaliação Turma", "📋 Matrículas"])

with tab1:
    aluno_nome = st.text_input("🎓 Nome do Aluno")
    col_a, col_b = st.columns(2)
    with col_a:
        p1 = st.radio("Desempenho Geral:", ["Totalmente compatível", "Parcialmente", "Abaixo", "Muito abaixo"], key="p1")
        p2 = st.radio("Evolução Período:", ["Significativa", "Gradual", "Pouca", "Inexistente"], key="p2")
        p3 = st.radio("Compreensão Conteúdo:", ["Plena", "Pequenas dificuldades", "Parcial", "Grandes dificuldades"], key="p3")
        p4 = st.radio("Ritmo Aprendizado:", ["Adequado", "Um pouco abaixo", "Abaixo", "Muito abaixo"], key="p4")
        p8 = st.radio("Atenção em Aula:", ["Constante", "Pequenas dispersões", "Frequente", "Raramente"], key="p8")
        p9 = st.radio("Autonomia Atividades:", ["Alta", "Média", "Baixa", "Inexistente"], key="p9")
    with col_b:
        p10 = st.radio("Postura Escolar:", ["Adequada", "Parcialmente", "Inadequada em momentos", "Frequente inadequada"], key="p10")
        p16 = st.radio("Extensão Dificuldades:", ["Pontuais", "Alguns componentes", "Vários componentes", "Generalizadas"], key="p16")
        p17 = st.radio("Foco da Dificuldade:", ["Conteúdo", "Interpretação", "Organização/Atenção", "Múltiplos fatores"], key="p17")
        p20 = st.radio("Comportamento afeta aprendizado?:", ["Não interfere", "Interfere ocasionalmente", "Interfere com frequência", "Compromete significativamente"], key="p20")
        p23 = st.radio("Acompanhamento Familiar:", ["Presente e efetivo", "Irregular", "Pouco presente", "Inexistente"], key="p23")
        coment_aluno = st.text_area("💬 Considerações do Professor (Observações Extras):", key="coment")

# --- BOTÃO DE AÇÃO ---
if st.button("🚀 SALVAR E GERAR RELATÓRIO INTELIGENTE", type="primary", use_container_width=True):
    if not prof or not aluno_nome:
        st.error("Por favor, preencha o nome do Professor e do Aluno!")
    else:
        # 1. Coletar Dados
        dados_finais = {
            "Data": datetime.datetime.now().strftime("%d/%m/%Y"), "Prof": prof, "Turma": turma_sel, "Aluno": aluno_nome,
            "p1": p1, "p2": p2, "p3": p3, "p4": p4, "p8": p8, "p9": p9, "p10": p10, "p16": p16, "p17": p17, "p20": p20, "p23": p23,
            "comentario": coment_aluno
        }
        
        try:
            # 2. Salvar no Google Sheets
            df_atual = conn.read(spreadsheet=url_planilha, ttl=0)
            df_atual = df_atual[[c for c in df_atual.columns if c in dados_finais.keys()]]
            df_final = pd.concat([df_atual, pd.DataFrame([dados_finais])], ignore_index=True)
            conn.update(spreadsheet=url_planilha, data=df_final)
            
            # 3. Gerar Texto com Gemini
            with st.spinner("🧠 O Gemini está analisando os dados e redigindo o relatório..."):
                texto_redigido = redigir_relatorio_ia(dados_finais)
            
            # 4. Criar Doc no Drive
            with st.spinner("📄 Criando o Documento Oficial no Google Docs..."):
                url_doc = gerar_google_doc(aluno_nome, turma_sel, texto_redigido)
            
            st.success("✅ Processo concluído com sucesso!")
            st.balloons()
            
            # Exibição dos resultados
            st.link_button("📂 ABRIR RELATÓRIO NO GOOGLE DOCS", url_doc)
            with st.expander("🔍 Visualizar rascunho do texto gerado"):
                st.write(texto_redigido)
                
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
