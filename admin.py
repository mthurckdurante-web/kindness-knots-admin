import streamlit as st
import pandas as pd
import os

# -------------------------------
# Configurações do Admin
# -------------------------------
ADMIN_PASSWORD = "sua_senha_secreta"

# Inicializar sessão para login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------------------------------
# Login
# -------------------------------
if not st.session_state.logged_in:
    st.title("Login Admin - Kindness Knots")
    senha_input = st.text_input("Digite a senha do admin", type="password")
    if st.button("Entrar"):
        if senha_input == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login realizado com sucesso!")
            st.experimental_rerun()
        else:
            st.error("Senha incorreta. Tente novamente.")
else:
    st.title("Painel Admin - Kindness Knots")

    # Criar pasta para imagens se não existir
    if not os.path.exists("imagens"):
        os.mkdir("imagens")

    # Carregar produtos
    try:
        produtos_df = pd.read_csv("produtos.csv")
    except:
        produtos_df = pd.DataFrame(columns=["nome", "categoria", "preco", "imagem"])

    # -------------------------------
    # Adicionar produto
    # -------------------------------
    st.header("Adicionar Produto")
    nome = st.text_input("Nome do Produto")
    categoria = st.selectbox("Categoria", ["Chaveiros", "Broches", "Pelúcias", "Amigurumis"])
    preco = st.number_input("Preço (R$)", min_value=0.0, step=0.1)
    imagem = st.file_uploader("Imagem do produto", type=["png", "jpg", "jpeg"])

    if st.button("Adicionar Produto"):
        if nome and imagem:
            imagem_path = f"imagens/{imagem.name}"
            with open(imagem_path, "wb") as f:
                f.write(imagem.getbuffer())
            produtos_df = pd.concat([produtos_df, pd.DataFrame([{
                "nome": nome,
                "categoria": categoria,
                "preco": preco,
                "imagem": imagem_path
            }])], ignore_index=True)
            produtos_df.to_csv("produtos.csv", index=False)
            st.success(f"Produto {nome} adicionado com sucesso!")
        else:
            st.error("Preencha o nome e envie a imagem do produto.")

    # -------------------------------
    # Editar ou remover produto
    # -------------------------------
    st.header("Editar / Remover Produto")
    if len(produtos_df) == 0:
        st.info("Nenhum produto cadastrado.")
    else:
        # Escolher produto
        opcoes = [f"{row['nome']} ({row['categoria']})" for idx, row in produtos_df.iterrows()]
        produto_selecionado = st.selectbox("Selecione o produto", opcoes)
        index = opcoes.index(produto_selecionado)
        produto = produtos_df.iloc[index]

        st.text_input("Nome", value=produto["nome"], key="edit_nome")
        st.selectbox("Categoria", ["Chaveiros", "Broches", "Pelúcias", "Amigurumis"], index=["Chaveiros", "Broches", "Pelúcias", "Amigurumis"].index(produto["categoria"]), key="edit_categoria")
        st.number_input("Preço (R$)", value=float(produto["preco"]), min_value=0.0, step=0.1, key="edit_preco")
        imagem_edit = st.file_uploader("Alterar imagem (opcional)", type=["png", "jpg", "jpeg"], key="edit_imagem")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Salvar Alterações"):
                produtos_df.at[index, "nome"] = st.session_state["edit_nome"]
                produtos_df.at[index, "categoria"] = st.session_state["edit_categoria"]
                produtos_df.at[index, "preco"] = st.session_state["edit_preco"]
                if imagem_edit:
                    imagem_path = f"imagens/{imagem_edit.name}"
                    with open(imagem_path, "wb") as f:
                        f.write(imagem_edit.getbuffer())
                    produtos_df.at[index, "imagem"] = imagem_path
                produtos_df.to_csv("produtos.csv", index=False)
                st.success("Produto atualizado com sucesso!")

        with col2:
            if st.button("Remover Produto"):
                produtos_df = produtos_df.drop(index)
                produtos_df.to_csv("produtos.csv", index=False)
                st.success("Produto removido com sucesso!")
