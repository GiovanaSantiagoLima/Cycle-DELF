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

# --- SEÇÃO REDIS (STREAK E VOCABULÁRIO) ---
st.divider()
st.subheader("🚀 Conquistas Rápidas (Redis)")

col_streak, col_vocab = st.columns(2)

# Testando a rota de Streak (Bitmap do Redis)
with col_streak:
    st.write("🔥 Sua Ofensiva")
    if st.button("Verificar minha constância"):
        # Chamada para a rota de finalizar/status que calcula o bitcount
        resp = requests.post(f"{API_URL}/sessao/finalizar/{user_id}")
        if resp.status_code == 200:
            dias = resp.json().get("dias_totais_no_ano")
            st.metric("Dias de estudo no ano", f"{dias} dias")
        else:
            st.error("Erro ao ler streak do Redis")

# Testando a rota de Vocabulário (HyperLogLog do Redis)
with col_vocab:
    st.write("🗣️ Estimativa de Vocabulário")
    novas_palavras = st.text_input("Adicionar palavras aprendidas (ex: maison, école)")
    if st.button("Atualizar Vocabulário"):
        if novas_palavras:
            lista = [p.strip() for p in novas_palavras.split(",")]
            resp = requests.post(f"{API_URL}/vocabulario/adicionar/{user_id}", json=lista)
            if resp.status_code == 200:
                total = resp.json().get("total_palavras_vistas_aproximadamente")
                st.info(f"Seu vocabulário estimado é de {total} palavras!")

if st.button("Material novo (Bloom Filter)"):
    resp = requests.get(f"{API_URL}/material/proximo/{user_id}")

    if resp.status_code == 200:
        data = resp.json()

        if "msg" in data:
            st.warning(data["msg"])
        else:
            st.success("Material novo encontrado!")
            st.write(data)