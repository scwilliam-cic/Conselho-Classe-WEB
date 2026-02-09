import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# Configuração da Página
st.set_page_config(page_title="Conselho de Classe Imaculada", layout="centered", page_icon="📝")

st.title("📝 Formulário de Conselho de Classe")

# Conexão com o Google Sheets
# Use o link da sua planilha aqui
url = "https://docs.google.com/spreadsheets/d/1bGcDE5Q-Dz0dhQgeqcHiLSS8WUqc2icvWb4k8SwxAwQ/edit#gid=0"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- DICIONÁRIOS DE DADOS (Mantendo seu roteiro original) ---
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

# --- INTERFACE ---
col1, col2 = st.columns(2)
with col1: prof = st.text_input("👤 Professor(a)")
with col2: turma_sel = st.selectbox("🏫 Turma", ["1º Ano A", "2º Ano A", "3º Ano A", "4º Ano A", "5º Ano A"])

aluno = st.text_input("🎓 Nome do Aluno")
resp_aluno = {"Data": datetime.datetime.now().strftime("%d/%m/%Y"), "Prof": prof, "Turma": turma_sel, "Aluno": aluno}

for sec, pergs in roteiro_aluno.items():
    st.subheader(sec)
    for p, opts in pergs.items():
        resp_aluno[p] = st.radio(p, opts, key=f"al_{p}")

st.markdown("---")

if st.button("💾 ENVIAR PARA PLANILHA CENTRAL", type="primary", use_container_width=True):
    if not prof or not aluno:
        st.error("Por favor, preencha o nome do Professor e do Aluno!")
    else:
        try:
            # 1. Lê os dados que já existem na planilha
            dados_existentes = conn.read(spreadsheet=url)
            
            # 2. Prepara a nova linha
            nova_linha = pd.DataFrame([resp_aluno])
            
            # 3. Junta o novo dado com os antigos
            tabela_final = pd.concat([dados_existentes, nova_linha], ignore_index=True)
            
            # 4. Atualiza a planilha no Google
            conn.update(spreadsheet=url, data=tabela_final)
            
            st.success("✅ Resposta enviada com sucesso para a planilha central!")
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")
