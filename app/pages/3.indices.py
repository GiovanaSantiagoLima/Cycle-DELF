import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Cycle DELF - Admin", page_icon="🔎")
st.title("🔎 Testes de Índices MongoDB")

option = st.sidebar.selectbox(
    "Escolha o teste de índice:",
    ["Busca por Texto", "Busca Geográfica", "Filtro Simples", "Ver Índices"]
)

if option == "Busca por Texto":
    st.header("📚 Busca de Materiais (Índice de Texto)")
    st.info("Busca palavras-chave no Título, Conteúdo e Competência.")
    q = st.text_input("Digite o termo de busca (ex: gastronomie):")
    
    if st.button("Buscar"):
        if q:
            resp = requests.get(f"{API_URL}/materials/search", params={"q": q.strip()})
            if resp.status_code == 200:
                results = resp.json()
                st.write(f"Encontrados: {len(results)}")
                st.json(results)
            else:
                st.error("Erro na busca")
        else:
            st.warning("Digite algo para buscar.")

elif option == "Busca Geográfica":
    st.header("🗺️ Usuários Próximos (Índice Geoespacial)")
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Latitude", value=-18.9186, format="%.6f")
    with col2:
        lon = st.number_input("Longitude", value=-48.2772, format="%.6f")
    
    radius = st.slider("Raio (km)", 1, 500, 50)
    
    if st.button("Buscar"):
        resp = requests.get(f"{API_URL}/users/nearby", params={"lat": lat, "lon": lon, "radius_km": radius})
        if resp.status_code == 200:
            st.json(resp.json())
        else:
            st.error("Erro na busca geográfica")

elif option == "Filtro Simples":
    st.header("👥 Filtrar Usuários (Índice Simples)")
    level = st.selectbox("Selecione o Nível:", ["A1", "A2", "B1", "B2", "C1", "C2"])
    
    if st.button("Filtrar"):
        resp = requests.get(f"{API_URL}/users/filter", params={"level": level})
        if resp.status_code == 200:
            results = resp.json()
            if not results:
                st.warning("Nenhum usuário encontrado com este nível. Verifique se há espaços extras no banco!")
            st.json(results)
        else:
            st.error("Erro ao filtrar")

elif option == "Ver Índices":
    st.header("⚙️ Índices Ativos no Banco")
    if st.button("Atualizar Lista"):
        resp = requests.get(f"{API_URL}/admin/indexes")
        if resp.status_code == 200:
            st.write(resp.json())