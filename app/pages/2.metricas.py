import streamlit as st
import requests
import pandas as pd

# Configurações de conexão
API_URL = "http://127.0.0.1:8000"

# 1. Título e Estilo
st.set_page_config(page_title="Métricas - Cycle DELF", page_icon="📊")
st.title("📊 Minha Evolução")

# 2. Verificação de Segurança (Garante que o app não quebre sem usuário)
if "user_id" not in st.session_state or not st.session_state.user_id:
    st.warning("⚠️ Usuário não identificado!")
    st.info("Por favor, selecione um usuário na página inicial antes de acessar as métricas.")
    if st.button("Ir para Home"):
        st.switch_page("1_home.py") # Ajuste para o nome exato do seu arquivo principal
    st.stop()

# Recupera dados da sessão
user_id = st.session_state.user_id
user_name = st.session_state.get("user_name", "Estudante")

st.markdown(f"Exibindo progresso de: **{user_name}**")
st.divider()

# Função auxiliar para chamadas de API com tratamento de erro
def get_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erro ao conectar com a API ({endpoint}): {e}")
        return []

# --- PROGRESSO MENSAL (GRÁFICO DE LINHA) ---
st.subheader("📈 Evolução das Notas")
monthly_data = get_data(f"analytics/monthly-progress/{user_id}")

if monthly_data:
    df_month = pd.DataFrame(monthly_data)
    # Criar coluna de data formatada para o eixo X
    df_month["data"] = df_month["_id"].apply(lambda x: f"{x['month']}/{x['year']}")
    
    # Gráfico de linha para o score
    st.line_chart(df_month.set_index("data")["avg_score"])
else:
    st.info("Você ainda não possui sessões suficientes para gerar o gráfico de evolução.")

# ---  ATIVIDADE POR COMPETÊNCIA (GRÁFICO DE BARRAS) ---
st.subheader("📚 Dedicação por Competência")
comp_data = get_data(f"analytics/activity-by-competence/{user_id}")

if comp_data:
    df_comp = pd.DataFrame(comp_data)
    df_comp = df_comp.rename(columns={"_id": "competencia", "sessions": "total_sessoes"})
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de barras mostrando onde você estuda mais (B1 focus)
        st.bar_chart(df_comp.set_index("competencia")["total_sessoes"])
    
    with col2:
        st.write("Resumo:")
        st.table(df_comp.set_index("competencia"))
else:
    st.info("Registre seu primeiro estudo para ver a distribuição por competência!")

# Botão para limpar cache e voltar
if st.sidebar.button("Trocar Usuário"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()