import streamlit as st
import requests
import json

# -------------------------------
# Configurações
# -------------------------------
FIREBASE_URL = "https://kindnessknots-c6b86-default-rtdb.firebaseio.com/produtos.json"  # Realtime Database
ADMIN_PASSWORD = "sua_senha_secreta"  # Troque para sua senha

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("Login Admin")
if not st.session_state.logged_in:
    senha = st.text_input("Senha do admin", type="password")
    if st.button("Entrar"):
        if senha == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login realizado!")
        else:
            st.error("Senha incorreta")

# -------------------------------
# Painel Admin
# -------------------------------
if st.session_state.logged_in:
    st.title("Painel Admin - Kindness Knots")

    st.header("Adicionar Produto")
    nome = st.text_input("Nome do Produto")
    categoria = st.selectbox("Categoria", ["Chaveiros", "Broches", "Pelúcias", "Amigurumis"])
    preco = st.number_input("Preço (R$)", min_value=0.0, step=0.1)
    url_imagem = st.text_input("URL da imagem")  # Agora precisa fornecer URL pública da imagem

    if st.button("Adicionar Produto"):
        if nome and url_imagem:
            produto = {
                "nome": nome,
                "categoria": categoria,
                "preco": preco,
                "imagem": url_imagem
            }
            response = requests.post(FIREBASE_URL, data=json.dumps(produto))
            if response.status_code == 200:
                st.success(f"Produto {nome} adicionado com sucesso!")
            else:
                st.error("Erro ao adicionar produto!")
        else:
            st.error("Preencha nome e URL da imagem")

    if st.button("Sair"):
        st.session_state.logged_in = False
        st.success("Você saiu do admin!")
