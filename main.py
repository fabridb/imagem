import streamlit as st
import openai

# Configurar a chave da API da OpenAI (recomenda usar secret manager em produção)
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "nop"

# Função para gerar o prompt
def gerar_prompt(nome_produto, preco, estilo_visual):
    return f"""
    Transforme esta foto realista de um {nome_produto} individual sobre uma bandeja de isopor em uma imagem publicitária de alta qualidade.

    Estilo de fotografia: {estilo_visual}, luz quente suave com sombras realistas, fundo desfocado (parede ou tecido marrom).

    Adicione vapores saindo do {nome_produto}, indicando que está quente. Use técnicas de food styling para destacar textura e brilho natural.

    Mantenha a composição centralizada e destaque o preço com tipografia elegante no canto inferior direito: R${preco:.2f}.

    No topo da imagem, adicione o texto “{nome_produto.title()}” com tipografia serifada, estilo editorial, discreta e sofisticada.

    Remova ruídos visuais da imagem original tais como sombra dura, objetos ao fundo, manchas, reflexos.
    """

# Função para gerar imagem com DALL-E 3
def gerar_imagem_dalle(prompt):
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response['data'][0]['url']
    except Exception as e:
        return str(e)

# Interface com Streamlit
st.set_page_config(page_title="Gerador de Imagens - Padaria", layout="centered")
st.title("Gerador Visual para Produtos de Padaria")
st.markdown("Crie imagens profissionais de produtos com base em fotos simples.")

# Entradas do usuário
nome = st.text_input("Nome do produto", "Bolo de Pamonha")
preco = st.number_input("Preço (R$)", min_value=0.0, value=7.00, step=0.50)
estilo = st.selectbox("Estilo visual", ["rústico", "moderno clean", "editorial"])
foto = st.file_uploader("Envie uma foto do produto", type=["jpg", "png", "jpeg"])

# Geração do prompt e imagem
if st.button("Gerar Imagem com IA"):
    if not foto:
        st.warning("Por favor, envie uma foto do produto.")
    else:
        prompt = gerar_prompt(nome, preco, estilo)
        st.subheader("Prompt gerado:")
        st.code(prompt)

        st.info("Gerando imagem com IA, aguarde alguns segundos...")
        url = gerar_imagem_dalle(prompt)

        if url.startswith("http"):
            st.image(url, caption="Imagem gerada com IA", use_column_width=True)
        else:
            st.error(f"Erro ao gerar imagem: {url}")
