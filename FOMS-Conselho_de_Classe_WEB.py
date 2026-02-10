import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Configuração da Página
st.set_page_config(page_title="Conselho de Classe Imaculada", layout="wide", page_icon="📝")

# 2. Conexão com Google Sheets
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

# --- ABA 1: ALUNO (30 PERGUNTAS + COMENTÁRIO) ---
with tab1:
    aluno_nome = st.text_input("🎓 Nome do Aluno")
    col_al1, col_al2 = st.columns(2)
    with col_al1:
        st.subheader("1. Perfil Geral")
        p1 = st.radio("O desempenho geral do aluno é:", ["Totalmente compatível com a série", "Parcialmente compatível", "Abaixo do esperado", "Muito abaixo do esperado"], key="al1")
        p2 = st.radio("Em relação à evolução ao longo do período, o aluno:", ["Apresentou evolução significativa", "Evoluiu de forma gradual", "Evoluiu pouco", "Não apresentou evolução"], key="al2")
        p3 = st.radio("Quanto à compreensão dos conteúdos essenciais, o aluno:", ["Compreende plenamente", "Compreende com pequenas dificuldades", "Compreende parcialmente", "Apresenta grandes dificuldades"], key="al3")
        p4 = st.radio("O ritmo de aprendizagem do aluno é:", ["Adequado", "Um pouco abaixo", "Abaixo do esperado", "Muito abaixo"], key="al4")
        p5 = st.radio("O desempenho do aluno indica:", ["Domínio dos objetivos de aprendizagem", "Atendimento parcial aos objetivos", "Atendimento mínimo", "Não atendimento aos objetivos"], key="al5")
        st.subheader("2. Engajamento")
        p6 = st.radio("A participação do aluno em sala é:", ["Frequente e ativa", "Regular", "Eventual", "Rara"], key="al6")
        p7 = st.radio("O interesse demonstrado pelo aluno é:", ["Elevado", "Moderado", "Baixo", "Muito baixo"], key="al7")
        p8 = st.radio("Quanto à atenção durante as aulas, o aluno:", ["Mantém atenção constante", "Apresenta pequenas dispersões", "Dispersa-se com frequência", "Raramente mantém atenção"], key="al8")
        p9 = st.radio("A autonomia do aluno na realização das atividades é:", ["Alta", "Média", "Baixa", "Inexistente"], key="al9")
        p10 = st.radio("A postura do aluno no ambiente escolar é:", ["Adequada", "Parcialmente adequada", "Inadequada em alguns momentos", "Frequentemente inadequada"], key="al10")
        st.subheader("3. Potencialidades")
        p11 = st.radio("O aluno demonstra potencial nas áreas:", ["Linguagem e comunicação", "Raciocínio lógico/matemático", "Criatividade e resolução de problemas", "Ainda não apresenta destaque evidente"], key="al11")
        p12 = st.radio("Em relação às orientações dos professores, o aluno:", ["Assimila e aplica", "Assimila parcialmente", "Demonstra dificuldade em aplicar", "Não demonstra assimilação"], key="al12")
        p13 = st.radio("O comprometimento com as atividades é:", ["Alto", "Moderado", "Baixo", "Muito baixo"], key="al13")
        p14 = st.radio("O aluno demonstra esforço mesmo diante de dificuldades?", ["Sempre", "Frequentemente", "Raramente", "Nunca"], key="al14")
        p15 = st.radio("O aluno apresenta:", ["Constância no desempenho", "Oscilações leves", "Oscilações frequentes", "Desempenho instável"], key="al15")
    with col_al2:
        st.subheader("4. Dificuldades")
        p16 = st.radio("As dificuldades apresentadas pelo aluno são:", ["Pontuais", "Em alguns componentes", "Em vários componentes", "Generalizadas"], key="al16")
        p17 = st.radio("As principais dificuldades estão relacionadas a:", ["Conteúdo específico", "Interpretação e compreensão", "Organização e atenção", "Múltiplos fatores"], key="al17")
        p18 = st.radio("Nas avaliações, o aluno:", ["Demonstra domínio do conteúdo", "Demonstra compreensão parcial", "Demonstra insegurança", "Responde de forma aleatória"], key="al18")
        p19 = st.radio("Em relação à leitura e interpretação de enunciados:", ["Não apresenta dificuldades", "Apresenta pequenas dificuldades", "Apresenta dificuldades frequentes", "Apresenta grandes dificuldades"], key="al19")
        p20 = st.radio("O comportamento do aluno:", ["Não interfere no aprendizado", "Interfere ocasionalmente", "Interfere com frequência", "Compromete significativamente"], key="al20")
        st.subheader("5. Causas")
        p21 = st.radio("As dificuldades parecem estar relacionadas a:", ["Defasagem anterior", "Falta de estudo", "Concentração", "Conjunto de fatores"], key="al21")
        p22 = st.radio("O aluno responde melhor quando:", ["Trabalha autônomo", "Recebe mediação", "Em grupo", "Acompanhamento individual"], key="al22")
        p23 = st.radio("O acompanhamento familiar é:", ["Presente e efetivo", "Presente, porém irregular", "Pouco presente", "Inexistente"], key="al23")
        p24 = st.radio("O aluno demonstra consciência de suas dificuldades?", ["Sim, claramente", "Parcialmente", "Pouco", "Não demonstra"], key="al24")
        p25 = st.radio("O aluno utiliza estratégias próprias para aprender?", ["Sim, com autonomia", "Às vezes", "Raramente", "Não utiliza"], key="al25")
        st.subheader("6. Intervenções")
        p26 = st.radio("As estratégias pedagógicas adotadas até o momento:", ["Eficazes", "Parcialmente eficazes", "Pouco eficazes", "Sem efeito"], key="al26")
        p27 = st.radio("O aluno necessita de:", ["Acompanhamento regular", "Reforço pontual", "Reforço contínuo", "Acompanhamento individualizado"], key="al27")
        p28 = st.radio("A recuperação da aprendizagem deve ocorrer:", ["Em sala", "Atividades complementares", "Atendimento específico", "Múltiplas frentes"], key="al28")
        p29 = st.radio("Recomenda-se:", ["Manutenção atual", "Ajustes pontuais", "Reestruturação", "Plano individual"], key="al29")
        p30 = st.radio("Considerando o conjunto, o aluno:", ["Bom aproveitamento", "Aproveitamento parcial", "Baixo aproveitamento", "Intervenção intensiva"], key="al30")

    st.divider()
    coment_aluno = st.text_area("💬 CONSIDERAÇÕES FINAIS (Individual):", placeholder="Escreva aqui observações extras sobre o aluno...")

# --- ABA 2: TURMA (20 PERGUNTAS + COMENTÁRIO) ---
with tab2:
    st.info(f"Avaliação da Turma: {turma_sel}")
    col_tr1, col_tr2 = st.columns(2)
    with col_tr1:
        st.subheader("1. Desempenho")
        t1 = st.radio("Desempenho geral da turma:", ["Muito satisfatório", "Satisfatório", "Parcialmente satisfatório", "Insatisfatório"], key="tr1")
        t2 = st.radio("Em relação à evolução ao longo do período letivo, a turma:", ["Apresentou evolução significativa", "Apresentou evolução gradual", "Evoluiu pouco", "Não apresentou evolução"], key="tr2")
        t3 = st.radio("A turma, de modo geral, compreende os conteúdos essenciais?", ["Compreende plenamente", "Compreende com pequenas dificuldades", "Compreende parcialmente", "Apresenta grandes dificuldades"], key="tr3")
        t4 = st.radio("O ritmo de aprendizagem da turma é:", ["Adequado", "Um pouco abaixo", "Abaixo", "Muito abaixo"], key="tr4")
        st.subheader("2. Participação")
        t5 = st.radio("A participação da turma nas atividades propostas é:", ["Ativa e constante", "Regular", "Irregular", "Baixa"], key="tr5")
        t6 = st.radio("O interesse da turma pelo processo de aprendizagem é:", ["Elevado", "Moderado", "Baixo", "Muito baixo"], key="tr6")
        t7 = st.radio("Quanto à atenção durante as aulas, a turma:", ["Mantém atenção constante", "Apresenta pequenas dispersões", "Dispersa-se com frequência", "Raramente mantém atenção"], key="tr7")
        t8 = st.radio("A autonomia da turma na realização das atividades é:", ["Alta", "Média", "Baixa", "Inexistente"], key="tr8")
        st.subheader("3. Organização")
        t9 = st.radio("A postura geral da turma em sala de aula é:", ["Adequada", "Parcialmente adequada", "Inadequada em alguns momentos", "Frequentemente inesperada"], key="tr9")
        t10 = st.radio("O cumprimento de tarefas e prazos pela turma é:", ["Regular e pontual", "Majoritariamente regular", "Irregular", "Raramente cumprido"], key="tr10")
    with col_tr2:
        t11 = st.radio("A organização de materiais e registros pela turma é:", ["Adequada", "Parcialmente adequada", "Pouco adequada", "Inadequada"], key="tr11")
        st.subheader("4. Avaliação")
        t12 = st.radio("Os resultados das avaliações indicam:", ["Bom domínio dos conteúdos", "Domínio parcial", "Baixo domínio", "Domínio insuficiente"], key="tr12")
        t13 = st.radio("A turma apresenta dificuldades significativas em:", ["Conteúdos pontuais", "Alguns componentes", "Vários componentes", "Dificuldades generalizadas"], key="tr13")
        t14 = st.radio("Em relação à leitura e interpretação de enunciados, a turma é:", ["Adequada", "Parcialmente adequada", "Deficiente", "Muito deficiente"], key="tr14")
        t15 = st.radio("O desempenho da turma ao longo do período foi:", ["Constante", "Com pequenas oscilações", "Com oscilações frequentes", "Instável"], key="tr15")
        st.subheader("5. Estratégias")
        t16 = st.radio("As estratégias pedagógicas atenderam às necessidades da turma?", ["Sim, plenamente", "Sim, parcialmente", "Pouco", "Não atenderam"], key="tr16")
        t17 = st.radio("A turma responde melhor a:", ["Aulas expositivas", "Atividades práticas/Dinâmicas", "Trabalhos em grupo", "Mediação constante"], key="tr17")
        t18 = st.radio("Há necessidade de replanejamento para a turma?", ["Não há necessidade", "Apenas ajustes pontuais", "Ajustes significativos", "Reestruturação total"], key="tr18")
        t19 = st.radio("Ações de recuperação da aprendizagem foram necessárias?", ["Não", "Pontuais", "Contínuas", "Intensivas"], key="tr19")
        t20 = st.radio("Considerando o conjunto, a turma apresenta:", ["Bom aproveitamento", "Aproveitamento satisfatório", "Aproveitamento parcial", "Baixo aproveitamento"], key="tr20")

    st.divider()
    coment_turma = st.text_area("💬 CONSIDERAÇÕES FINAIS (Turma):", placeholder="Escreva aqui observações gerais sobre o desempenho da turma...")

# --- BOTÃO DE ENVIO WEB ---
st.markdown("---")
if st.button("💾 ENVIAR RESPOSTAS PARA PLANILHA CENTRAL", type="primary", use_container_width=True):
    if not prof:
        st.error("⚠️ Preencha o nome do Professor!")
    elif not aluno_nome and "al1" in st.session_state:
         st.error("⚠️ Preencha o nome do Aluno!")
    else:
        try:
            if aluno_nome:
                dados = {
                    "Data": datetime.datetime.now().strftime("%d/%m/%Y"), "Prof": prof, "Turma": turma_sel, "Aluno": aluno_nome,
                    "O desempenho geral do aluno é:": p1, "Em relação à evolução ao longo do período, o aluno:": p2, "Quanto à compreensão dos conteúdos essenciais, o aluno:": p3, "O ritmo de aprendizagem do aluno é:": p4, "O desempenho do aluno indica:": p5,
                    "A participação do aluno em sala é:": p6, "O interesse demonstrado pelo aluno é:": p7, "Quanto à atenção durante as aulas, o aluno:": p8, "A autonomia do aluno na realização das atividades é:": p9, "A postura do aluno no ambiente escolar é:": p10,
                    "O aluno demonstra potencial nas áreas:": p11, "Em relação às orientações dos professores, o aluno:": p12, "O comprometimento com as atividades é:": p13, "O aluno demonstra esforço mesmo diante de dificuldades?": p14, "O aluno apresenta:": p15,
                    "As dificuldades apresentadas pelo aluno são:": p16, "As principais dificuldades estão relacionadas a:": p17, "Nas avaliações, o aluno:": p18, "Em relação à leitura e interpretação de enunciados:": p19, "O comportamento do aluno:": p20,
                    "As dificuldades parecem estar relacionadas a:": p21, "O aluno responde melhor quando:": p22, "O acompanhamento familiar é:": p23, "O aluno demonstra consciência de suas dificuldades?": p24, "O aluno utiliza estratégias próprias para aprender?": p25,
                    "As estratégias pedagógicas adotadas até o momento:": p26, "O aluno necessita de:": p27, "A recuperação da aprendizagem deve ocorrer:": p28, "Recomenda-se:": p29, "Considerando o conjunto, o aluno:": p30,
                    "CONSIDERAÇÕES FINAIS": coment_aluno
                }
            else:
                dados = {
                    "Data": datetime.datetime.now().strftime("%d/%m/%Y"), "Prof": prof, "Turma": turma_sel, "Aluno": "COLETIVO",
                    "Desempenho geral da turma:": t1, "Em relação à evolução ao longo do período letivo, a turma:": t2, "A turma, de modo geral, compreende os conteúdos essenciais?": t3, "O ritmo de aprendizagem da turma é:": t4, "A participação da turma nas atividades propostas é:": t5,
                    "O interesse da turma pelo processo de aprendizagem é:": t6, "Quanto à atenção durante as aulas, a turma:": t7, "A autonomia da turma na realização das atividades é:": t8, "A postura geral da turma em sala de aula é:": t9, "O cumprimento de tarefas e prazos pela turma é:": t10,
                    "A organização de materiais e registros pela turma é:": t11, "Os resultados das avaliações indicam:": t12, "A turma apresenta dificuldades significativas em:": t13, "Em relação à leitura e interpretação de enunciados, a turma é:": t14, "O desempenho da turma ao longo do período foi:": t15,
                    "As estratégias pedagógicas atenderam às necessidades da turma?": t16, "A turma responde melhor a:": t17, "Há necessidade de replanejamento para a turma?": t18, "Ações de recuperação da aprendizagem foram necessárias?": t19, "Considerando o conjunto, a turma apresenta:": t20,
                    "CONSIDERAÇÕES FINAIS": coment_turma
                }
            df_atual = conn.read(spreadsheet=url, ttl=0)
            df_final = pd.concat([df_atual, pd.DataFrame([dados])], ignore_index=True)
            df_final = df_final.loc[:, ~df_final.columns.str.contains('^Unnamed')]
            conn.update(spreadsheet=url, data=df_final)
            st.success("✅ Gravado com sucesso na planilha central!")
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao gravar: {e}")
