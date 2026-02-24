import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Configuração da Página
st.set_page_config(page_title="Conselho de Classe Imaculada", layout="wide", page_icon="📝")

# 2. Conexão com Google Sheets (Usando a nova biblioteca corrigida)
conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1bGcDE5Q-Dz0dhQgeqcHiLSS8WUqc2icvWb4k8SwxAwQ/edit#gid=1477512121"

st.title("📝 Formulário de Conselho de Classe")

# --- IDENTIFICAÇÃO ---
c1, c2 = st.columns(2)
with c1: 
    prof = st.text_input("👤 Nome do Professor(a)")
with c2: 
    turma_sel = st.selectbox("🏫 Turma", ["1º Ano A", "2º Ano A", "3º Ano A", "4º Ano A", "5º Ano A"])

# Abas do Formulário
tab1, tab2, tab3 = st.tabs(["🎓 Avaliação Aluno", "👥 Avaliação Turma", "📋 Consulta de Matrículas"])

# --- ABA 1: ALUNO (30 PERGUNTAS) ---
with tab1:
    aluno_nome = st.text_input("🎓 Nome do Aluno")
    col_al1, col_al2 = st.columns(2)
    
    with col_al1:
        p1 = st.radio("1. O desempenho geral do aluno é:", ["Totalmente compatível com a série", "Parcialmente compatível", "Abaixo do esperado", "Muito abaixo do esperado"], key="al1")
        p2 = st.radio("2. Em relação à evolução ao longo do período, o aluno:", ["Apresentou evolução significativa", "Evoluiu de forma gradual", "Evoluiu pouco", "Não apresentou evolução"], key="al2")
        p3 = st.radio("3. Quanto à compreensão dos conteúdos essenciais, o aluno:", ["Compreende plenamente", "Compreende com pequenas dificuldades", "Compreende parcialmente", "Apresenta grandes dificuldades"], key="al3")
        p4 = st.radio("4. O ritmo de aprendizagem do aluno é:", ["Adequado", "Um pouco abaixo", "Abaixo do esperado", "Muito abaixo"], key="al4")
        p5 = st.radio("5. O desempenho do aluno indica:", ["Domínio dos objetivos de aprendizagem", "Atendimento parcial aos objetivos", "Atendimento mínimo", "Não atendimento aos objetivos"], key="al5")
        p6 = st.radio("6. A participação do aluno em sala é:", ["Frequente e ativa", "Regular", "Eventual", "Rara"], key="al6")
        p7 = st.radio("7. O interesse demonstrado pelo aluno é:", ["Elevado", "Moderado", "Baixo", "Muito baixo"], key="al7")
        p8 = st.radio("8. Quanto à atenção durante as aulas, o aluno:", ["Mantém atenção constante", "Apresenta pequenas dispersões", "Dispersa-se com frequência", "Raramente mantém atenção"], key="al8")
        p9 = st.radio("9. A autonomia do aluno na realização das atividades é:", ["Alta", "Média", "Baixa", "Inexistente"], key="al9")
        p10 = st.radio("10. A postura do aluno no ambiente escolar é:", ["Adequada", "Parcialmente adequada", "Inadequada em alguns momentos", "Frequentemente inadequada"], key="al10")
        p11 = st.radio("11. O aluno demonstra potencial nas áreas:", ["Linguagem e comunicação", "Raciocínio lógico/matemático", "Criatividade e resolução de problemas", "Ainda não apresenta destaque evidente"], key="al11")
        p12 = st.radio("12. Em relação às orientações dos professores, o aluno:", ["Assimila e aplica", "Assimila parcialmente", "Demonstra dificuldade em aplicar", "Não demonstra assimilação"], key="al12")
        p13 = st.radio("13. O comprometimento com as atividades é:", ["Alto", "Moderado", "Baixo", "Muito baixo"], key="al13")
        p14 = st.radio("14. O aluno demonstra esforço mesmo diante de dificuldades?", ["Sempre", "Frequentemente", "Raramente", "Nunca"], key="al14")
        p15 = st.radio("15. O aluno apresenta:", ["Constância no desempenho", "Oscilações leves", "Oscilações frequentes", "Desempenho instável"], key="al15")

    with col_al2:
        p16 = st.radio("16. As dificuldades apresentadas pelo aluno são:", ["Pontuais", "Em alguns componentes", "Em vários componentes", "Generalizadas"], key="al16")
        p17 = st.radio("17. As principais dificuldades estão relacionadas a:", ["Conteúdo específico", "Interpretação e compreensão", "Organização e atenção", "Múltiplos fatores"], key="al17")
        p18 = st.radio("18. Nas avaliações, o aluno:", ["Demonstra domínio do conteúdo", "Demonstra compreensão parcial", "Demonstra insegurança", "Responde de forma aleatória"], key="al18")
        p19 = st.radio("19. Em relação à leitura e interpretação de enunciados:", ["Não apresenta dificuldades", "Apresenta pequenas dificuldades", "Apresenta dificuldades frequentes", "Apresenta grandes dificuldades"], key="al19")
        p20 = st.radio("20. O comportamento do aluno:", ["Não interfere no aprendizado", "Interfere ocasionalmente", "Interfere com frequência", "Compromete significativamente"], key="al20")
        p21 = st.radio("21. As dificuldades parecem estar relacionadas a:", ["Defasagem anterior", "Falta de estudo", "Concentração", "Conjunto de fatores"], key="al21")
        p22 = st.radio("22. O aluno responde melhor quando:", ["Trabalha autônomo", "Recebe mediação", "Em grupo", "Acompanhamento individual"], key="al22")
        p23 = st.radio("23. O acompanhamento familiar é:", ["Presente e efetivo", "Presente, porém irregular", "Pouco presente", "Inexistente"], key="al23")
        p24 = st.radio("24. O aluno demonstra consciência de suas dificuldades?", ["Sim, claramente", "Parcialmente", "Pouco", "Não demonstra"], key="al24")
        p25 = st.radio("25. O aluno utiliza estratégias próprias para aprender?", ["Sim, com autonomia", "Às vezes", "Raramente", "Não utiliza"], key="al25")
        p26 = st.radio("26. As estratégias pedagógicas adotadas até o momento:", ["Eficazes", "Parcialmente eficazes", "Pouco eficazes", "Sem efeito"], key="al26")
        p27 = st.radio("27. O aluno necessita de:", ["Acompanhamento regular", "Reforço pontual", "Reforço contínuo", "Acompanhamento individualizado"], key="al27")
        p28 = st.radio("28. A recuperação da aprendizagem deve ocorrer:", ["Em sala", "Atividades complementares", "Atendimento específico", "Múltiplas frentes"], key="al28")
        p29 = st.radio("29. Recomenda-se:", ["Manutenção atual", "Ajustes pontuais", "Reestruturação", "Plano individual"], key="al29")
        p30 = st.radio("30. Considerando o conjunto, o aluno:", ["Bom aproveitamento", "Aproveitamento parcial", "Baixo aproveitamento", "Intervenção intensiva"], key="al30")
    
    coment_aluno = st.text_area("💬 CONSIDERAÇÕES FINAIS (Individual):", key="cal")

# --- ABA 2: TURMA (20 PERGUNTAS) ---
with tab2:
    col_tr1, col_tr2 = st.columns(2)
    with col_tr1:
        t1 = st.radio("1. Desempenho geral da turma:", ["Muito satisfatório", "Satisfatório", "Parcialmente satisfatório", "Insatisfatório"], key="tr1")
        t2 = st.radio("2. Em relação à evolução ao longo do período letivo, a turma:", ["Apresentou evolução significativa", "Apresentou evolução gradual", "Evoluiu pouco", "Não apresentou evolução"], key="tr2")
        t3 = st.radio("3. A turma, de modo geral, compreende os conteúdos essenciais?", ["Compreende plenamente", "Compreende com pequenas dificuldades", "Compreende parcialmente", "Apresenta grandes dificuldades"], key="tr3")
        t4 = st.radio("4. O ritmo de aprendizagem da turma é:", ["Adequado", "Um pouco abaixo", "Abaixo", "Muito abaixo"], key="tr4")
        t5 = st.radio("5. A participação da turma nas atividades propostas é:", ["Ativa e constante", "Regular", "Irregular", "Baixa"], key="tr5")
        t6 = st.radio("6. O interesse da turma pelo processo de aprendizagem é:", ["Elevado", "Moderado", "Baixo", "Muito baixo"], key="tr6")
        t7 = st.radio("7. Quanto à atenção durante as aulas, a turma:", ["Mantém atenção constante", "Apresenta pequenas dispersões", "Dispersa-se com frequência", "Raramente mantém atenção"], key="tr7")
        t8 = st.radio("8. A autonomia da turma na realização das atividades é:", ["Alta", "Média", "Baixa", "Inexistente"], key="tr8")
        t9 = st.radio("9. A postura geral da turma em sala de aula é:", ["Adequada", "Parcialmente adequada", "Inadequada em alguns momentos", "Frequentemente inesperada"], key="tr9")
        t10 = st.radio("10. O cumprimento de tarefas e prazos pela turma é:", ["Regular e pontual", "Majoritariamente regular", "Irregular", "Raramente cumprido"], key="tr10")
    
    with col_tr2:
        t11 = st.radio("11. A organização de materiais e registros pela turma é:", ["Adequada", "Parcialmente adequada", "Pouco adequada", "Inadequada"], key="tr11")
        t12 = st.radio("12. Os resultados das avaliações indicam:", ["Bom domínio dos conteúdos", "Domínio parcial", "Baixo domínio", "Domínio insuficiente"], key="tr12")
        t13 = st.radio("13. A turma apresenta dificuldades significativas em:", ["Conteúdos pontuais", "Alguns componentes", "Vários componentes", "Dificuldades generalizadas"], key="tr13")
        t14 = st.radio("14. Em relação à leitura e interpretação de enunciados, a turma é:", ["Adequada", "Parcialmente adequada", "Deficiente", "Muito deficiente"], key="tr14")
        t15 = st.radio("15. O desempenho da turma ao longo do período foi:", ["Constante", "Com pequenas oscilações", "Com oscilações frequentes", "Instável"], key="tr15")
        t16 = st.radio("16. As estratégias pedagógicas atenderam às necessidades da turma?", ["Sim, plenamente", "Sim, parcialmente", "Pouco", "Não atenderam"], key="tr16")
        t17 = st.radio("17. A turma responde melhor a:", ["Aulas expositivas", "Atividades práticas/Dinâmicas", "Trabalhos em grupo", "Mediação constante"], key="tr17")
        t18 = st.radio("18. Há necessidade de replanejamento para a turma?", ["Não há necessidade", "Apenas ajustes pontuais", "Ajustes significativos", "Reestruturação total"], key="tr18")
        t19 = st.radio("19. Ações de recuperação da aprendizagem foram necessárias?", ["Não", "Pontuais", "Contínuas", "Intensivas"], key="tr19")
        t20 = st.radio("20. Considerando o conjunto, a turma apresenta:", ["Bom aproveitamento", "Aproveitamento satisfatório", "Aproveitamento parcial", "Baixo aproveitamento"], key="tr20")
    
    coment_turma = st.text_area("💬 CONSIDERAÇÕES FINAIS (Turma):", key="ctr")

# --- ABA 3: MATRÍCULAS ---
with tab3:
    st.subheader("📋 Relação de Alunos e Matrículas")
    try:
        df_mat = conn.read(spreadsheet=url, worksheet="Matriculas", ttl=0)
        busca = st.text_input("🔍 Buscar aluno pelo nome:", key="busca_mat")
        if busca:
            df_mat = df_mat[df_mat.iloc[:, 0].astype(str).str.contains(busca, case=False, na=False)]
        st.dataframe(df_mat, use_container_width=True, hide_index=True)
    except:
        st.info("Para exibir dados aqui, crie uma aba chamada 'Matriculas' na sua planilha.")

# --- BOTÃO DE ENVIO ---
if st.button("💾 ENVIAR RESPOSTAS PARA PLANILHA CENTRAL", type="primary", use_container_width=True):
    try:
        if aluno_nome:
            dados = {
                "Data": datetime.datetime.now().strftime("%d/%m/%Y"), "Prof": prof, "Turma": turma_sel, "Aluno": aluno_nome,
                "p1": p1, "p2": p2, "p3": p3, "p4": p4, "p5": p5, "p6": p6, "p7": p7, "p8": p8, "p9": p9, "p10": p10,
                "p11": p11, "p12": p12, "p13": p13, "p14": p14, "p15": p15, "p16": p16, "p17": p17, "p18": p18, "p19": p19, "p20": p20,
                "p21": p21, "p22": p22, "p23": p23, "p24": p24, "p25": p25, "p26": p26, "p27": p27, "p28": p28, "p29": p29, "p30": p30,
                "CONSIDERAÇÕES FINAIS": coment_aluno
            }
        else:
            dados = {
                "Data": datetime.datetime.now().strftime("%d/%m/%Y"), "Prof": prof, "Turma": turma_sel, "Aluno": "COLETIVO",
                "t1": t1, "t2": t2, "t3": t3, "t4": t4, "t5": t5, "t6": t6, "t7": t7, "t8": t8, "t9": t9, "t10": t10,
                "t11": t11, "t12": t12, "t13": t13, "t14": t14, "t15": t15, "t16": t16, "t17": t17, "t18": t18, "t19": t19, "t20": t20,
                "CONSIDERAÇÕES FINAIS": coment_turma
            }
        
        # Lendo os dados atuais para adicionar o novo
        df_atual = conn.read(spreadsheet=url, ttl=0)
        df_final = pd.concat([df_atual, pd.DataFrame([dados])], ignore_index=True)
        conn.update(spreadsheet=url, data=df_final)
        
        st.success("✅ Gravado com sucesso na Planilha!")
        st.balloons()
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
