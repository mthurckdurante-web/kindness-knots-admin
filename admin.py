import streamlit as st
import pandas as pd
import urllib.parse

# Carregar produtos
try:
    produtos_df = pd.read_csv("produtos.csv")
except:
    st.warning("Nenhum produto disponível no momento.")
    produtos_df = pd.DataFrame(columns=["nome", "categoria", "preco", "imagem"])

st.title("Kindness Knots - Loja")

# Selecionar categoria
categoria_selecionada = st.selectbox("Escolha a categoria", ["Chaveiros", "Broches", "Pelúcias", "Amigurumis"])
produtos_categoria = produtos_df[produtos_df["categoria"] == categoria_selecionada]

for i, produto in produtos_categoria.iterrows():
    st.subheader(produto["nome"])
    st.image(produto["imagem"], width=200)
    st.write(f"Preço: R${produto['preco']}")
    
    # Botão de compra
    if st.button(f"Comprar {produto['nome']}", key=f"btn_{i}"):
        with st.form(key=f"form_{i}"):
            st.write("Finalize sua compra:")
            nome_cliente = st.text_input("Seu nome")
            telefone = st.text_input("Telefone")
            endereco = st.text_area("Endereço")
            cidade = st.text_input("Cidade")
            
            # Modo de entrega automático
            modo_entrega = "Uber Entrega" if cidade.strip().lower() == "taubate" else "Correios"
            
            submit = st.form_submit_button("Finalizar Compra")
            
            if submit:
                # Montar mensagem
                mensagem = (
                    f"Olá! Gostaria de comprar:\n"
                    f"Produto: {produto['nome']}\n"
                    f"Nome: {nome_cliente}\n"
                    f"Telefone: {telefone}\n"
                    f"Endereço: {endereco}\n"
                    f"Modo de Entrega: {modo_entrega}"
                )
                
                # Codificar a mensagem para URL
                mensagem_url = urllib.parse.quote(mensagem)
                
                # Link para DM via Instagram (abre o perfil, usuário pode copiar a mensagem)
                instagram_user = "kindnessknots"
                url = f"https://www.instagram.com/{instagram_user}/"
                
                st.success("Clique no botão abaixo para enviar sua mensagem via DM do Instagram:")
                st.markdown(f"[Abrir Instagram]({url})", unsafe_allow_html=True)
                st.info("Copie a mensagem abaixo para enviar pelo DM:")
                st.code(mensagem)
