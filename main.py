import streamlit as st
import openai

# Configurar a chave da API da OpenAI (use secret manager em produção)
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", None)

if not OPENAI_API_KEY:
    st.error("Chave da API da OpenAI não configurada. Adicione-a em st.secrets ou como variável de ambiente.")
    st.stop()

openai.api_key = OPENAI_API_KEY

# Função para gerar o prompt
def gerar_prompt(nome_produto, preco, estilo_visual):
    return (
        f"Uma imagem publicitária de um {nome_produto} em um prato branco com acabamento artesanal, no estilo {estilo_visual}. "
        f"Use iluminação suave, fundo desfocado neutro, e vapores sutis indicando que o produto está quente. "
        f"Adicione o texto '{nome_produto.title()}' no topo com fonte serifada elegante e o preço 'R${preco}' no canto inferior direito."
    )

# Função para gerar imagem com DALL·E 3
def gerar_imagem_dalle(prompt):
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1  # DALL·E 3 suporta apenas n=1
        )
        return response.data[0].url
    except openai.OpenAIError as e:
        return f"Erro da API OpenAI: {str(e)}"
    except Exception as e:
        return f"Erro inesperado: {str(e)}"

# Interface com Streamlit
st.set_page_config(page_title="Gerador de Imagens - Padaria", layout="centered")
st.title("Gerador Visual para Produtos de Padaria")
st.markdown("Crie imagens profissionais de produtos a partir de descrições.")

# Entradas do usuário
nome = st.text_input("Nome do produto", "Bolo de Pamonha")
preco = st.text_input("Preço (R$)", "7.00")
estilo = st.selectbox("Estilo visual", ["rústico", "moderno clean", "editorial"])
foto = st.file_uploader("Envie uma foto do produto (opcional)", type=["jpg", "png", "jpeg"])

# Geração do prompt e imagem
if st.button("Gerar Imagem com IA"):
    if not nome or not preco:
        st.error("Por favor, preencha o nome do produto e o preço.")
    else:
        prompt = gerar_prompt(nome, preco, estilo)
        st.subheader("Prompt gerado:")
        st.code(prompt)

        st.info("Gerando imagem com IA, aguarde alguns segundos...")
        url = gerar_imagem_dalle(prompt)

        if isinstance(url, str) and url.startswith("http"):
            st.image(url, caption="Imagem gerada com IA", use_column_width=True)
        else:
            st.error(f"Erro ao gerar imagem: {url}")
