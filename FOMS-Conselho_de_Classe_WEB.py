import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

# Configuração da Página
st.set_page_config(page_title="Conselho de Classe Imaculada", layout="centered", page_icon="📝")

st.title("📝 Formulário de Conselho de Classe")

# --- DICIONÁRIOS DE DADOS ---
roteiro_aluno = {
    "1. Perfil Geral do Aluno": {
        "O desempenho geral do aluno é:": ["Totalmente compatível com a série", "Parcialmente compatível", "Abaixo do esperado", "Muito abaixo do esperado"],
        "Em relação à evolução ao longo do período, o aluno:": ["Apresentou evolução significativa", "Evoluiu de forma gradual", "Evoluiu pouco", "Não apresentou evolução"],
        "Quanto à compreensão dos conteúdos essenciais, o aluno:": ["Compreende plenamente", "Compreende com pequenas dificuldades", "Compreende parcialmente", "Apresenta grandes dificuldades"],
        "O ritmo de aprendizagem do aluno é:": ["Adequado", "Um pouco abaixo", "Abaixo do esperado", "Muito abaixo"],
        "O desempenho do aluno indica:": ["Domínio dos objetivos de aprendizagem", "Atendimento parcial aos objetivos", "Atendimento mínimo", "Não atendimento aos objetivos"]
    },
    "2. Engajamento e Postura": {
        "A participação do aluno em sala é:": ["Frequente e ativa", "Regular", "Eventual", "Rara"],
        "O interesse demonstrado pelo aluno é:": ["Elevado", "Moderado", "Baixo", "Muito baixo"],
        "Quanto à atenção durante as aulas, o aluno:": ["Mantém atenção constante", "Apresenta pequenas dispersões", "Dispersa-se com frequência", "Raramente mantém atenção"],
        "A autonomia do aluno na realização das atividades é:": ["Alta", "Média", "Baixa", "Inexistente"],
        "A postura do aluno no ambiente escolar é:": ["Adequada", "Parcialmente adequada", "Inadequada em alguns momentos", "Frequentemente inadequada"]
    },
    "3. Potencialidades (Pontos Positivos)": {
        "O aluno demonstra potencial nas áreas:": ["Linguagem e comunicação", "Raciocínio lógico/matemático", "Criatividade e resolução de problemas", "Ainda não apresenta destaque evidente"],
        "Em relação às orientações dos professores, o aluno:": ["Assimila e aplica", "Assimila parcialmente", "Demonstra dificuldade em aplicar", "Não demonstra assimilação"],
        "O comprometimento com as atividades é:": ["Alto", "Moderado", "Baixo", "Muito baixo"],
        "O aluno demonstra esforço mesmo diante de dificuldades?": ["Sempre", "Frequentemente", "Raramente", "Nunca"],
        "O aluno apresenta:": ["Constância no desempenho", "Oscilações leves", "Oscilações frequentes", "Desempenho instável"]
    },
    "4. Dificuldades Identificadas": {
        "As dificuldades apresentadas pelo aluno são:": ["Pontuais", "Em alguns componentes", "Em vários componentes", "Generalizadas"],
        "As principais dificuldades estão relacionadas a:": ["Conteúdo específico", "Interpretação e compreensão", "Organização e atenção", "Múltiplos fatores"],
        "Nas avaliações, o aluno:": ["Demonstra domínio do conteúdo", "Demonstra compreensão parcial", "Demonstra insegurança", "Responde de forma aleatória"],
        "Em relação à leitura e interpretação de enunciados:": ["Não apresenta dificuldades", "Apresenta pequenas dificuldades", "Apresenta dificuldades frequentes", "Apresenta grandes dificuldades"],
        "O comportamento do aluno:": ["Não interfere no aprendizado", "Interfere ocasionalmente", "Interfere com frequência", "Compromete significativamente"]
    },
    "5. Causas Prováveis": {
        "As dificuldades parecem estar relacionadas a:": ["Defasagem de conteúdos anteriores", "Falta de estudo sistemático", "Dificuldades de concentração", "Conjunto de fatores"],
        "O aluno responde melhor quando:": ["Trabalha de forma autônoma", "Recebe mediação do professor", "Realiza atividades em grupo", "Recebe acompanhamento individual"],
        "O acompanhamento familiar é:": ["Presente e efetivo", "Presente, porém irregular", "Pouco presente", "Inexistente"],
        "O aluno demonstra consciência de suas dificuldades?": ["Sim, claramente", "Parcialmente", "Pouco", "Não demonstra"],
        "O aluno utiliza estratégias próprias para aprender?": ["Sim, com autonomia", "Às vezes", "Raramente", "Não utiliza"]
    },
    "6. Intervenções e Encaminhamentos": {
        "As estratégias pedagógicas adotadas até o momento:": ["Foram eficazes", "Foram parcialmente eficazes", "Pouco eficazes", "Não surtiram efeito"],
        "O aluno necessita de:": ["Acompanhamento regular", "Reforço pontual", "Reforço contínuo", "Acompanhamento individualizado"],
        "A recuperação da aprendizagem deve ocorrer:": ["Em sala de aula", "Em atividades complementares", "Em atendimento específico", "Em múltiplas frentes"],
        "Para melhor aproveitamento, recomenda-se:": ["Manutenção das estratégias atuais", "Ajustes pedagógicos pontuais", "Reestruturação das estratégias", "Plano de intervenção individual"],
        "Considerando o conjunto das análises, o aluno:": ["Apresenta bom aproveitamento", "Apresenta aproveitamento parcial", "Apresenta baixo aproveitamento", "Necessita intervenção intensiva"]
    }
}

roteiro_turma = {
    "1. Desempenho Geral da Turma": {
        "O desempenho geral da turma é:": ["Muito satisfatório", "Satisfatório", "Parcialmente satisfatório", "Insatisfatório"],
        "Em relação à evolução ao longo do período letivo, a turma:": ["Apresentou evolução significativa", "Apresentou evolução gradual", "Evoluiu pouco", "Não apresentou evolução"],
        "A turma, de modo geral, compreende os conteúdos essenciais?": ["Compreende plenamente", "Compreende com pequenas dificuldades", "Compreende parcialmente", "Apresenta grandes dificuldades"],
        "O ritmo de aprendizagem da turma é:": ["Adequado", "Um pouco abaixo do esperado", "Abaixo do esperado", "Muito abaixo do esperado"]
    },
    "2. Participação e Engajamento Coletivo": {
        "A participação da turma nas atividades propostas é:": ["Ativa e constante", "Regular", "Irregular", "Baixa"],
        "O interesse da turma pelo processo de aprendizagem é:": ["Elevado", "Moderado", "Baixo", "Muito baixo"],
        "Quanto à atenção durante as aulas, a turma:": ["Mantém atenção constante", "Apresenta pequenas dispersões", "Dispersa-se com frequência", "Raramente mantém atenção"],
        "A autonomia da turma na realização das atividades é:": ["Alta", "Média", "Baixa", "Muito baixa"]
    },
    "3. Organização e Postura da Turma": {
        "A postura geral da turma em sala de aula é:": ["Adequada", "Parcialmente adequada", "Inadequada em alguns momentos", "Frequentemente inesperada"],
        "O cumprimento de tarefas e prazos pela turma é:": ["Regular e pontual", "Majoritariamente regular", "Irregular", "Raramente cumprido"],
        "A organização dos materiais e registros da turma é:": ["Adequada", "Parcialmente adequada", "Pouco adequada", "Inadequada"]
    },
    "4. Avaliação e Aprendizagem": {
        "Os resultados das avaliações da turma indicam:": ["Bom domínio dos conteúdos", "Domínio parcial", "Baixo domínio", "Domínio insuficiente"],
        "A turma apresenta dificuldades significativas em:": ["Conteúdos pontuais", "Alguns componentes curriculares", "Vários componentes curriculares", "De forma generalizada"],
        "A interpretação de enunciados pela turma é:": ["Adequada", "Parcialmente adequada", "Deficiente", "Muito deficiente"],
        "O desempenho da turma ao longo do período é:": ["Constante", "Com pequenas oscilações", "Com oscilações frequentes", "Muito instável"]
    },
    "5. Estratégias Pedagógicas e Encaminhamentos": {
        "As estratégias pedagógicas adotadas atenderam às necessidades da turma?": ["Sim, plenamente", "Sim, parcialmente", "Pouco", "Não atenderam"],
        "A turma responde melhor a:": ["Aulas expositivas", "Atividades práticas e dinâmicas", "Trabalhos em grupo", "Mediação constante do professor"],
        "Há necessidade de replanejamento das práticas pedagógicas?": ["Não há necessidade", "Pequenos ajustes", "Ajustes significativos", "Reestruturação do planejamento"],
        "A turma necessita de ações de recuperação da aprendizagem?": ["Não", "Pontuais", "Contínuas", "Intensivas"],
        "Considerando o conjunto das análises, a turma:": ["Apresenta bom aproveitamento", "Apresenta aproveitamento satisfatório", "Apresenta aproveitamento parcial", "Apresenta baixo aproveitamento"]
    }
}

# --- INTERFACE ---
col1, col2 = st.columns(2)
with col1: prof = st.text_input("👤 Professor(a)")
with col2: turma_sel = st.selectbox("🏫 Turma", ["1º Ano A", "2º Ano A", "3º Ano A", "4º Ano A", "5º Ano A"])

tab1, tab2 = st.tabs(["Avaliação Aluno (Individual)", "Avaliação Turma (Coletiva)"])

with tab1:
    aluno = st.text_input("🎓 Nome do Aluno")
    resp_aluno = {"Data": datetime.datetime.now().strftime("%d/%m/%Y"), "Prof": prof, "Turma": turma_sel, "Aluno": aluno}
    for sec, pergs in roteiro_aluno.items():
        st.subheader(sec)
        for p, opts in pergs.items():
            resp_aluno[p] = st.radio(p, opts, key=f"al_{p}")

with tab2:
    st.info(f"Avaliação da Turma: {turma_sel}")
    resp_turma = {"Data": datetime.datetime.now().strftime("%d/%m/%Y"), "Prof": prof, "Turma": turma_sel}
    for sec, pergs in roteiro_turma.items():
        st.subheader(sec)
        for p, opts in pergs.items():
            resp_turma[p] = st.radio(p, opts, key=f"tr_{p}")

st.markdown("---")
if st.button("💾 FINALIZAR E GERAR PLANILHA", type="primary", use_container_width=True):
    if not prof or (not aluno and "Aluno" in resp_aluno):
        st.error("Por favor, preencha o nome do Professor e do Aluno!")
    else:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            pd.DataFrame([resp_aluno]).to_excel(writer, index=False, sheet_name='Aluno')
            pd.DataFrame([resp_turma]).to_excel(writer, index=False, sheet_name='Turma')
        
        st.success("Planilha gerada com sucesso!")
        st.download_button(
            label="⬇️ Baixar Excel",
            data=output.getvalue(),
            file_name=f"Conselho_{turma_sel}_{datetime.date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )