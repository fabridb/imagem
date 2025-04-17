import streamlit as st
import openai

# Configurar a chave da API da OpenAI (recomenda usar secret manager em produção)
openai.api_key = st.secrets.get("OPENAI_API_KEY", "sua-chave-aqui")

# Função para gerar o prompt
def gerar_prompt(nome_produto, preco, estilo_visual):
    return (
        f"Crie uma imagem publicitária de um {nome_produto} sobre um prato branco com acabamento artesanal em estilo {estilo_visual}. "
        f"Use luz suave e fundo desfocado de tom neutro, inclua vapores saindo do produto para indicar que está quente. "
        f"Adicione o texto {nome_produto.title()} na parte superior com fonte serifada elegante e destaque o preço R${preco} no canto inferior direito."
    )

# Função para gerar imagem com DALL·E (utilizando a API estável)
def gerar_imagem_dalle(prompt):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response["data"][0]["url"]
    except Exception as e:
        return str(e)

# Interface com Streamlit
st.set_page_config(page_title="Gerador de Imagens - Padaria", layout="centered")
st.title("Gerador Visual para Produtos de Padaria")
st.markdown("Crie imagens profissionais de produtos com base em textos descritivos.")

# Entradas do usuário
nome = st.text_input("Nome do produto", "Bolo de Pamonha")
preco = st.text_input("Preço (R$)", "7,00")
estilo = st.selectbox("Estilo visual", ["rústico", "moderno clean", "editorial"])
foto = st.file_uploader("Envie uma foto do produto", type=["jpg", "png", "jpeg"])

# Geração do prompt e imagem
if st.button("Gerar Imagem com IA"):
    prompt = gerar_prompt(nome, preco, estilo)
    st.subheader("Prompt gerado:")
    st.code(prompt)

    st.info("Gerando imagem com IA, aguarde alguns segundos...")
    url = gerar_imagem_dalle(prompt)

    if isinstance(url, str) and url.startswith("http"):
        st.image(url, caption="Imagem gerada com IA", use_column_width=True)
    else:
        st.error(f"Erro ao gerar imagem: {url}")
