import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="CycleDELF", layout="wide")

st.title("🎓 CycleDELF Learning Dashboard")

st.markdown("Plataforma de acompanhamento de aprendizado de francês.")

# -------------------
# Usuários mais ativos
# -------------------
st.subheader("🏆 Usuários mais ativos")

try:
    top_users = requests.get(f"{API_URL}/analytics/top-users").json()
    users = requests.get(f"{API_URL}/users").json()

    user_map = {u["_id"]: u.get("name", "Usuário") for u in users}

    data = []
    for u in top_users:
        name = user_map.get(u["_id"], "Usuário")
        data.append({
            "Usuário": name,
            "Sessões": u["total_sessions"]
        })

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

except:
    st.warning("API não está rodando.")