
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Controle de Estoque", page_icon="📦")

st.title("📦 Controle de Estoque")
st.write("Cadastre produtos e acompanhe o valor do estoque.")

# Guarda os produtos durante a sessão
if "produtos" not in st.session_state:
    st.session_state.produtos = []

# Formulário de cadastro
with st.form("form_produto"):
    produto = st.text_input("Nome do produto")
    preco = st.number_input("Preço unitário (R$)", min_value=0.0, step=1.0)
    quantidade = st.number_input(
        "Quantidade em estoque", min_value=0, step=1
    )

    cadastrar = st.form_submit_button("Cadastrar produto")

if cadastrar:
    if not produto.strip():
        st.error("Digite o nome do produto.")
    elif preco <= 0:
        st.error("O preço deve ser maior que zero.")
    elif quantidade <= 0:
        st.error("A quantidade deve ser maior que zero.")
    else:
        estoque = preco * quantidade

        st.session_state.produtos.append({
            "Produto": produto,
            "Preço unitário": preco,
            "Quantidade": quantidade,
            "Valor em estoque": estoque
        })

        st.success(f"{produto} cadastrado!")

# Exibe os produtos cadastrados
if st.session_state.produtos:
    st.subheader("Produtos cadastrados")

    df = pd.DataFrame(st.session_state.produtos)
    st.dataframe(df, use_container_width=True)

    total_geral = df["Valor em estoque"].sum()
    st.metric("Valor total do estoque", f"R$ {total_geral:.2f}")

    st.subheader("Situação do estoque")

    for item in st.session_state.produtos:
        if item["Quantidade"] < 5:
            st.warning(f"{item['Produto']}: estoque baixo!")
        else:
            st.success(f"{item['Produto']}: estoque suficiente.")
else:
    st.info("Ainda não há produtos cadastrados.")
