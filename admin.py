import streamlit as st
import requests
import json

# Configurações Firebase
FIREBASE_DB_URL = "https://kindnessknots-c6b86-default-rtdb.firebaseio.com/produtos.json"
FIREBASE_STORAGE_URL = "https://firebasestorage.googleapis.com/v0/b/kindnessknots-c6b86.appspot.com/o/"

ADMIN_PASSWORD = "2828"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login admin
st.title("Login Admin")
if not st.session_state.logged_in:
    senha = st.text_input("Senha do admin", type="password")
    if st.button("Entrar"):
        if senha == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login realizado!")
        else:
            st.error("Senha incorreta")

# Painel admin
if st.session_state.logged_in:
    st.header("Adicionar Produto")

    nome = st.text_input("Nome do Produto")
    categoria = st.selectbox("Categoria", ["Chaveiros", "Broches", "Pelúcias", "Amigurumis"])
    preco = st.number_input("Preço (R$)", min_value=0.0, step=0.1)

    # Upload de imagem
    uploaded_file = st.file_uploader("Escolha a imagem do produto", type=["png", "jpg", "jpeg"])
    
    if st.button("Adicionar Produto"):
        if not nome or not uploaded_file:
            st.error("Preencha o nome e escolha uma imagem")
        else:
            # Upload da imagem para Firebase Storage
            file_name = uploaded_file.name
            storage_url = f"{FIREBASE_STORAGE_URL}{file_name}"
            params = {"uploadType": "media", "name": file_name}
            headers = {"Content-Type": uploaded_file.type}

            r = requests.post(storage_url, params=params, headers=headers, data=uploaded_file.read())
            
            if r.status_code in [200, 201]:
                # Cria produto no Realtime Database
                produto = {
                    "nome": nome,
                    "categoria": categoria,
                    "preco": preco,
                    "imagem": f"{FIREBASE_STORAGE_URL}{file_name}?alt=media"
                }
                response = requests.post(FIREBASE_DB_URL, data=json.dumps(produto))
                if response.status_code == 200:
                    st.success("Produto adicionado com sucesso!")
                else:
                    st.error("Erro ao salvar produto no banco!")
            else:
                st.error("Erro ao enviar a imagem para o Firebase Storage")
