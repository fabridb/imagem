import streamlit as st
import openai

# Configurar a chave da API da OpenAI (recomenda usar secret manager em produção)
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "sua-chave-aqui"

# Função para gerar o prompt
def gerar_prompt(nome_produto, preco, estilo_visual):
    return (
        f"Crie uma imagem publicitária de um {nome_produto} sobre um prato branco, com acabamento artesanal, em estilo {estilo_visual}. "
        f"Utilize luz suave e fundo desfocado de tom neutro. Inclua vapores saindo do produto, destacando que está quente. "
        f"Adicione o texto {nome_produto.title()} na parte superior com fonte serifada elegante, e destaque o preço R${preco:.2f} no canto inferior direito."
    )

# Função para gerar imagem com DALL·E 3 (compatível com openai >= 1.12.0)
def gerar_imagem_dalle(prompt):
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024"
        )
        image_url = response.data[0].url  # A nova API retorna dessa forma
        return image_url
    except Exception as e:
        return str(e)

# Interface com Streamlit
st.set_page_config(page_title="Gerador de Imagens - Padaria", layout="centered")
st.title("Gerador Visual para Produtos")
st.markdown("Crie imagens profissionais de produtos com base em fotos simples.")

# Entradas do usuário
nome = st.text_input("Nome do produto", "Bolo de Pamonha")
preco = st.number_input("Preço (R$)", min_value=0.0, value=7.00, step=0.50)
estilo = st.selectbox("Estilo visual", ["rústico", "moderno clean", "editorial"])
foto = st.file_uploader("Envie uma foto do produto", type=["jpg", "png", "jpeg"])

# Geração do prompt e imagem
if st.button("Gerar Imagem com IA"):
    if not foto:
        st.warning("Por favor, envie uma foto do produto (opcional). A IA não processa a imagem diretamente, apenas gera com base no texto.")
    prompt = gerar_prompt(nome, preco, estilo)
    st.subheader("Prompt gerado:")
    st.code(prompt)

    st.info("Gerando imagem com IA, aguarde alguns segundos...")
    url = gerar_imagem_dalle(prompt)

    if isinstance(url, str) and url.startswith("http"):
        st.image(url, caption="Imagem gerada com IA", use_column_width=True)
    else:
        st.error(f"Erro ao gerar imagem: {url}")
