import streamlit as st
import firebase_admin
from firebase_admin import credentials, db, storage

# -------------------------------
# Configuração Firebase
# -------------------------------
cred = credentials.Certificate("firebase_credentials.json")  # coloque este JSON na mesma pasta
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://kindnessknots-c6b86-default-rtdb.firebaseio.com/",
    "storageBucket": "kindnessknots-c6b86.appspot.com"
})

bucket = storage.bucket()

# -------------------------------
# Login Admin
# -------------------------------
ADMIN_PASSWORD = "2828"  # Troque para sua senha
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
    imagem = st.file_uploader("Imagem do produto", type=["png","jpg","jpeg"])

    if st.button("Adicionar Produto"):
        if nome and imagem:
            # Salvar imagem no Firebase Storage
            blob = bucket.blob(imagem.name)
            blob.upload_from_file(imagem)
            blob.make_public()
            url_imagem = blob.public_url

            # Salvar produto no Realtime Database
            ref = db.reference("produtos")
            produto = {
                "nome": nome,
                "categoria": categoria,
                "preco": preco,
                "imagem": url_imagem
            }
            ref.push(produto)
            st.success(f"Produto {nome} adicionado com sucesso!")
        else:
            st.error("Preencha o nome e envie uma imagem")

    if st.button("Sair"):
        st.session_state.logged_in = False
        st.success("Você saiu do admin!")

