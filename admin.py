import streamlit as st
import pandas as pd
import os

# -------------------------------
# Configuração da senha do admin
# -------------------------------
ADMIN_PASSWORD = "2828"  # Troque para a senha que quiser

# -------------------------------
# Inicializar estado da sessão
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------------------------------
# Funções auxiliares
# -------------------------------
def carregar_produtos():
    try:
        return pd.read_csv("produtos.csv")
    except:
        return pd.DataFrame(columns=["nome", "categoria", "preco", "imagem"])

def salvar_produtos(df):
    df.to_csv("produtos.csv", index=False)

# -------------------------------
# Login
# -------------------------------
st.title("Login Admin - Kindness Knots")

if not st.session_state.logged_in:
    senha_input = st.text_input("Digite a senha do admin", type="password", key="login_senha")
    if st.button("Entrar", key="login_btn"):
        if senha_input == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login realizado com sucesso!")
        else:
            st.error("Senha incorreta. Tente novamente.")

# -------------------------------
# Conteúdo do painel admin
# -------------------------------
if st.session_state.logged_in:
    st.title("Painel Admin - Kindness Knots")

    # Criar pasta para imagens se não existir
    if not os.path.exists("imagens"):
        os.mkdir("imagens")

    # Carregar produtos
    produtos_df = carregar_produtos()

    # -------------------------------
    # Adicionar produto
    # -------------------------------
    st.header("Adicionar Produto")
    nome = st.text_input("Nome do Produto", key="add_nome")
    categoria = st.selectbox("Categoria", ["Chaveiros", "Broches", "Pelúcias", "Amigurumis"], key="add_categoria")
    preco = st.number_input("Preço (R$)", min_value=0.0, step=0.1, key="add_preco")
    imagem = st.file_uploader("Imagem do produto", type=["png", "jpg", "jpeg"], key="add_imagem")

    if st.button("Adicionar Produto", key="btn_add"):
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
            salvar_produtos(produtos_df)
            st.success(f"Produto {nome} adicionado com sucesso!")
        else:
            st.error("Preencha o nome e envie a imagem do produto.")

    # -------------------------------
    # Editar / Remover produto
    # -------------------------------
    st.header("Editar / Remover Produto")
    if len(produtos_df) == 0:
        st.info("Nenhum produto cadastrado.")
    else:
        opcoes = [f"{row['nome']} ({row['categoria']})" for idx, row in produtos_df.iterrows()]
        produto_selecionado = st.selectbox("Selecione o produto", opcoes, key="edit_select")
        index = opcoes.index(produto_selecionado)
        produto = produtos_df.iloc[index]

        nome_edit = st.text_input("Nome", value=produto["nome"], key=f"edit_nome_{index}")
        categoria_edit = st.selectbox("Categoria", ["Chaveiros","Broches","Pelúcias","Amigurumis"],
                                      index=["Chaveiros","Broches","Pelúcias","Amigurumis"].index(produto["categoria"]),
                                      key=f"edit_categoria_{index}")
        preco_edit = st.number_input("Preço (R$)", value=float(produto["preco"]), min_value=0.0, step=0.1, key=f"edit_preco_{index}")
        imagem_edit = st.file_uploader("Alterar imagem (opcional)", type=["png","jpg","jpeg"], key=f"edit_imagem_{index}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Salvar Alterações", key=f"btn_save_{index}"):
                produtos_df.at[index, "nome"] = nome_edit
                produtos_df.at[index, "categoria"] = categoria_edit
                produtos_df.at[index, "preco"] = preco_edit
                if imagem_edit:
                    imagem_path = f"imagens/{imagem_edit.name}"
                    with open(imagem_path, "wb") as f:
                        f.write(imagem_edit.getbuffer())
                    produtos_df.at[index, "imagem"] = imagem_path
                salvar_produtos(produtos_df)
                st.success("Produto atualizado com sucesso!")

        with col2:
            if st.button("Remover Produto", key=f"btn_remove_{index}"):
                produtos_df = produtos_df.drop(index)
                salvar_produtos(produtos_df)
                st.success("Produto removido com sucesso!")

    # -------------------------------
    # Logout
    # -------------------------------
    if st.button("Sair", key="btn_logout"):
        st.session_state.logged_in = False
        st.success("Você saiu com sucesso!")
