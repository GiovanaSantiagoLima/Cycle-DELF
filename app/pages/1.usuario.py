import streamlit as st
import requests
import random

API_URL = "http://127.0.0.1:8000"

st.title("📚 Estudar")

# -------------------
# Criar usuário
# -------------------
st.subheader("Criar usuário")

name = st.text_input("Nome")
level = st.selectbox("Nível", ["A1", "A2", "B1", "B2"])

if st.button("Criar usuário"):
    requests.post(f"{API_URL}/users", json={"name": name, "level": level})
    st.success("Usuário criado!")

# -------------------
# Selecionar usuário
# -------------------
users = requests.get(f"{API_URL}/users").json()
user_map = {u["name"]: u["_id"] for u in users if "name" in u}

selected = st.selectbox("Usuário atual", list(user_map.keys()))

if selected:
    # GRAVAR NO SESSION STATE PARA AS OUTRAS PÁGINAS ACESSAREM
    st.session_state.user_id = user_map[selected]
    st.session_state.user_name = selected
    
    st.success(f"Usuário: {selected}")
    user_id = st.session_state.user_id # Define para uso local

# -------------------
# Escolher competência
# -------------------
competence = st.selectbox(
    "Competência",
    [
        "Comprehension Écrite",
        "Compreension Orale",
        "Production Écrite",
        "Production Orale"
    ]
)

# -------------------
# Buscar materiais
# -------------------
if st.button("Buscar material para estudar"):
    try:
        materials = requests.get(f"{API_URL}/materials").json()
        filtered = [m for m in materials if isinstance(m, dict) and m.get("competence") == competence]

        if not filtered:
            st.warning("Nenhum material encontrado")
        else:
            st.session_state["material"] = random.choice(filtered)
    except:
        st.error("Erro ao conectar com o servidor.")

# -------------------
# Estudo
# -------------------
if "material" in st.session_state:
    material = st.session_state["material"]
    st.markdown("---")
    st.subheader("Material recomendado")
    
    st.info(material.get("content"))

    duration = st.number_input("Tempo de estudo (minutos)", 1, 120, 10)

    # --- SEÇÃO DE AUTOAVALIAÇÃO COM SCORE ---
    if "Production" in competence:
        st.subheader("Autoavaliação")
        
        with st.expander("📊 Critérios para sua nota", expanded=True):
            st.markdown("""
            **Como definir seu score:**
            * **90-100:** Usei o *futur antérieur* sem erros e o vocabulário foi variado.
            * **70-89:** Cometi erros leves de conjugação, mas a mensagem está clara.
            * **50-69:** Esqueci a estrutura formal ou errei muitos particípios.
            * **Abaixo de 50:** Tive muita dificuldade em estruturar as frases.
            """)
        
        # O slider agora faz sentido porque você tem uma "tabela" acima para se basear
        score = st.slider("Qual nota você se dá baseada nos critérios acima?", 0, 100, 70)
    else:
        # Para compreensão (Écrite/Orale), se não houver exercício de marcar, 
        # o slider serve para o quão bem você entendeu o conteúdo.
        score = st.slider("Nível de compreensão (0-100%)", 0, 100, 80)

    if st.button("Finalizar estudo"):
        try:
            start = requests.post(f"{API_URL}/sessions/start/{user_id}").json()
            session_id = start["session_id"]

            requests.post(
                f"{API_URL}/sessions/finish/{session_id}",
                json={
                    "duration_minutes": duration,
                    "score": score,
                    "competence": competence
                }
            )

            st.success(f"Sessão salva! Score de {score} registrado.")
            del st.session_state["material"]
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao conectar com a API: {e}")