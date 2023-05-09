import openai, dotenv, os
dotenv.load_dotenv() 
# Initialize the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_resposta(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=messages,
        max_tokens=1024,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]

mensagens = [{"role": "system", "content": "Você é um assistente gente boa."}]

while True:
    # Ask a question
    keywords = ["gato", "gata", "gatas", "gatos", "felino", "felinos", "miau", "miado"] 
    question = input("Perguntar pro ChatGPT (\"sair\"): ")

    if question == "sair" or question == "":
        print("saindo")
        break
    else:
        if (word in question.lower() for word in keywords):
            mensagens.append({"role": "user", "content": str(question)})
            answer = gerar_resposta(mensagens)
            print("Você:", question)
            print("ChatGPT:", answer[0])
            mensagens.append({"role": "assistant", "content": answer[0]})
        else:
            print("Desculpe, mas as perguntas devem ser relacionadas a gatos. Tente novamente!")

    debugar = False
    if debugar:
        print("Mensagens", mensagens, type(mensagens))
