import openai, dotenv, os

dotenv.load_dotenv()  # variáveis de ambiente do arquivo .env

openai.api_key = os.getenv("OPENAI_API_KEY")

def chatgpt(contexto, pergunta):
    # lista de palavras-chave relacionadas a gatos
    keywords = ["gato", "gatos", "felino", "felinos", "miau", "miado"] 

    # verifica se pelo menos uma palavra-chave está presente na pergunta
    if not any(word in pergunta.lower() for word in keywords):
        return "Desculpe, mas as perguntas devem ser relacionadas a gatos. Tente novamente!"

    prompt = f'{contexto}. {pergunta}. Forneça uma resposta objetiva e curta.'

    completions = openai.Completion.create(
        engine="davinci", 
        prompt=prompt, 
        max_tokens=200, 
        n=1, 
        stop=None, 
        temperature=0.1,
    )
    
    message = completions.choices[0].text.strip()
    return message


# o contexto podem ser dados que o usuário fornece previamente através de um formulário
contexto = "Eu tenho um gato siamês de 2 anos chamado Tom. Ele é muito brincalhão e adora perseguir bolas de papel."
pergunta = "Como cuidar de gatos filhotes?"

resposta = chatgpt(contexto, pergunta)
print(resposta)