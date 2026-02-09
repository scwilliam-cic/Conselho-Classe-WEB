import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Configuração da Página
st.set_page_config(page_title="Conselho de Classe Imaculada", layout="wide", page_icon="📝")

# 2. Conexão com Google Sheets (Configurada via Secrets no Streamlit Cloud)
conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1bGcDE5Q-Dz0dhQgeqcHiLSS8WUqc2icvWb4k8SwxAwQ/edit#gid=1477512121"

st.title("📝 Formulário de Conselho de Classe")

# --- IDENTIFICAÇÃO ---
c1, c2 = st.columns(2)
with c1: 
    prof = st.text_input("👤 Nome do Professor(a)")
with c2: 
    turma_sel = st.selectbox("🏫 Turma", ["1º Ano A", "2º Ano A", "3º Ano A", "4º Ano A", "5º Ano A"])

tab1, tab2 = st.tabs(["🎓 Avaliação Aluno (Individual)", "👥 Avaliação Turma (Coletiva)"])

# --- ABA 1: ALUNO (30 PERGUNTAS) ---
with tab1:
    aluno_nome = st.text_input("🎓 Nome do Aluno")
    res_al = {"Data": datetime.datetime.now().strftime("%d/%m/%Y"), "Prof": prof, "Turma": turma_sel, "Aluno": aluno_nome, "Tipo": "Individual"}
    
    col_al1, col_al2 = st.columns(2)
    with col_al1:
        st.subheader("1. Perfil Geral")
        res_al["A1"] = st.radio("O desempenho geral é:", ["Totalmente compatível", "Parcialmente", "Abaixo do esperado", "Muito abaixo"], key="al1")
        res_al["A2"] = st.radio("Evolução no período:", ["Significativa", "Gradual", "Pouca", "Não apresentou"], key="al2")
        res_al["A3"] = st.radio("Compreensão de conteúdos:", ["Plena", "Pequenas dificuldades", "Parcial", "Grandes dificuldades"], key="al3")
        res_al["A4"] = st.radio("Ritmo de aprendizagem:", ["Adequado", "Um pouco abaixo", "Abaixo", "Muito abaixo"], key="al4")
        res_al["A5"] = st.radio("Atendimento aos objetivos:", ["Domínio total", "Parcial", "Mínimo", "Não atendimento"], key="al5")
        st.subheader("2. Engajamento")
        res_al["A6"] = st.radio("Participação em sala:", ["Frequente e ativa", "Regular", "Eventual", "Rara"], key="al6")
        res_al["A7"] = st.radio("Interesse demonstrado:", ["Elevado", "Moderado", "Baixo", "Muito baixo"], key="al7")
        res_al["A8"] = st.radio("Atenção nas aulas:", ["Constante", "Pequenas dispersões", "Frequentes", "Rara"], key="al8")
        res_al["A9"] = st.radio("Autonomia:", ["Alta", "Média", "Baixa", "Inexistente"], key="al9")
        res_al["A10"] = st.radio("Postura escolar:", ["Adequada", "Parcialmente", "Inadequada", "Muito inadequada"], key="al10")
        st.subheader("3. Potencialidades")
        res_al["A11"] = st.radio("Demonstra potencial em:", ["Linguagem", "Raciocínio", "Criatividade", "Nenhuma área evidente"], key="al11")
        res_al["A12"] = st.radio("Assimila orientações:", ["Sim", "Parcialmente", "Com dificuldade", "Não"], key="al12")
        res_al["A13"] = st.radio("Comprometimento:", ["Alto", "Moderado", "Baixo", "Muito baixo"], key="al13")
        res_al["A14"] = st.radio("Esforço nas dificuldades:", ["Sempre", "Frequentemente", "Raramente", "Nunca"], key="al14")
        res_al["A15"] = st.radio("Constância:", ["Constante", "Oscilações leves", "Oscilações frequentes", "Instável"], key="al15")

    with col_al2:
        st.subheader("4. Dificuldades")
        res_al["A16"] = st.radio("As dificuldades são:", ["Pontuais", "Alguns componentes", "Vários", "Generalizadas"], key="al16")
        res_al["A17"] = st.radio("Relacionadas a:", ["Conteúdo", "Interpretação", "Organização", "Múltiplos fatores"], key="al17")
        res_al["A18"] = st.radio("Nas avaliações:", ["Domina", "Parcial", "Insegurança", "Aleatório"], key="al18")
        res_al["A19"] = st.radio("Leitura/Interpretação:", ["Sem dificuldades", "Pequenas", "Frequentes", "Grandes"], key="al19")
        res_al["A20"] = st.radio("Comportamento:", ["Não interfere", "Ocasional", "Interfere", "Compromete"], key="al20")
        st.subheader("5. Causas")
        res_al["A21"] = st.radio("Causa provável:", ["Defasagem", "Falta de estudo", "Concentração", "Emocional"], key="al21")
        res_al["A22"] = st.radio("Responde melhor:", ["Autônomo", "Mediação", "Em grupo", "Individual"], key="al22")
        res_al["A23"] = st.radio("Família:", ["Efetiva", "Irregular", "Pouco presente", "Inexistente"], key="al23")
        res_al["A24"] = st.radio("Consciência dificuldade:", ["Sim", "Parcialmente", "Pouco", "Não"], key="al24")
        res_al["A25"] = st.radio("Estratégias próprias:", ["Sim", "Às vezes", "Raramente", "Não"], key="al25")
        st.subheader("6. Intervenções")
        res_al["A26"] = st.radio("Estratégias adotadas:", ["Eficazes", "Parciais", "Pouco eficazes", "Sem efeito"], key="al26")
        res_al["A27"] = st.radio("Necessita de:", ["Acompanhamento", "Reforço pontual", "Reforço contínuo", "Individualizado"], key="al27")
        res_al["A28"] = st.radio("Recuperação:", ["Em sala", "Complementar", "Específica", "Múltiplas"], key="al28")
        res_al["A29"] = st.radio("Recomenda-se:", ["Manutenção", "Ajustes", "Reestruturação", "Plano individual"], key="al29")
        res_al["A30"] = st.radio("Conclusão:", ["Bom aproveitamento", "Parcial", "Baixo", "Urgente"], key="al30")

# --- ABA 2: TURMA (20 PERGUNTAS) ---
with tab2:
    st.info(f"Avaliação da Turma: {turma_sel}")
    res_tr = {"Data": datetime.datetime.now().strftime("%d/%m/%Y"), "Prof": prof, "Turma": turma_sel, "Aluno": "---", "Tipo": "Turma"}
    col_tr1, col_tr2 = st.columns(2)
    with col_tr1:
        st.subheader("1. Desempenho")
        res_tr["T1"] = st.radio("Desempenho da turma:", ["Muito satisfatório", "Satisfatório", "Parcial", "Insatisfatório"], key="tr1")
        res_tr["T2"] = st.radio("Evolução:", ["Significativa", "Gradual", "Pouca", "Não houve"], key="tr2")
        res_tr["T3"] = st.radio("Compreensão coletiva:", ["Plena", "Pequenas dificuldades", "Parcial", "Grandes"], key="tr3")
        res_tr["T4"] = st.radio("Ritmo da turma:", ["Adequado", "Pouco abaixo", "Abaixo", "Muito abaixo"], key="tr4")
        st.subheader("2. Participação")
        res_tr["T5"] = st.radio("Participação coletiva:", ["Ativa", "Regular", "Irregular", "Baixa"], key="tr5")
        res_tr["T6"] = st.radio("Interesse:", ["Elevado", "Moderado", "Baixo", "Muito baixo"], key="tr6")
        res_tr["T7"] = st.radio("Atenção:", ["Constante", "Pequenas dispersões", "Frequentes", "Rara"], key="tr7")
        res_tr["T8"] = st.radio("Autonomia coletiva:", ["Alta", "Média", "Baixa", "Muito baixa"], key="tr8")
        st.subheader("3. Postura")
        res_tr["T9"] = st.radio("Postura em sala:", ["Adequada", "Parcialmente", "Inadequada", "Inesperada"], key="tr9")
        res_tr["T10"] = st.radio("Prazos e tarefas:", ["Regular", "Majoritariamente", "Irregular", "Raramente"], key="tr10")
    with col_tr2:
        res_tr["T11"] = st.radio("Organização material:", ["Adequada", "Parcialmente", "Pouco", "Inadequada"], key="tr11")
        st.subheader("4. Resultados")
        res_tr["T12"] = st.radio("Avaliações indicam:", ["Bom domínio", "Parcial", "Baixo", "Insuficiente"], key="tr12")
        res_tr["T13"] = st.radio("Dificuldade em:", ["Conteúdos pontuais", "Alguns", "Vários", "Generalizada"], key="tr13")
        res_tr["T14"] = st.radio("Interpretação:", ["Adequada", "Parcial", "Deficiente", "Muito deficiente"], key="tr14")
        res_tr["T15"] = st.radio("Constância da turma:", ["Constante", "Pequenas oscilações", "Frequentes", "Instável"], key="tr15")
        st.subheader("5. Estratégias")
        res_tr["T16"] = st.radio("Atendimento necessidades:", ["Sim", "Parcialmente", "Pouco", "Não"], key="tr16")
        res_tr["T17"] = st.radio("Respondem melhor a:", ["Expositivas", "Práticas", "Grupo", "Mediação"], key="tr17")
        res_tr["T18"] = st.radio("Replanejamento:", ["Não há", "Pequenos", "Significativos", "Reestruturação"], key="tr18")
        res_tr["T19"] = st.radio("Recuperação:", ["Não", "Pontuais", "Contínuas", "Intensivas"], key="tr19")
        res_tr["T20"] = st.radio("Aproveitamento final:", ["Bom", "Satisfatório", "Parcial", "Baixo"], key="tr20")

# --- BOTÃO DE ENVIO WEB ---
st.markdown("---")
if st.button("💾 ENVIAR RESPOSTAS PARA PLANILHA CENTRAL", type="primary", use_container_width=True):
    if not prof:
        st.error("⚠️ Preencha o nome do Professor!")
    else:
        try:
            dados_para_salvar = res_al if aluno_nome else res_tr
            df_atual = conn.read(spreadsheet=url, ttl=0)
            df_final = pd.concat([df_atual, pd.DataFrame([dados_para_salvar])], ignore_index=True)
            conn.update(spreadsheet=url, data=df_final)
            st.success("✅ Gravado com sucesso na nuvem!")
            st.balloons()
        except Exception as e:
            st.error(f"Erro de permissão: {e}. Verifique os Secrets e se o bot é EDITOR na planilha.")
