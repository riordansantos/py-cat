import tkinter as tk
import openai, dotenv, os
import wikipedia

# define o título da página da Wikipedia que você deseja pesquisar
page_title = "Gato"

# pesquisa o conteúdo da página da Wikipedia
contexto = wikipedia.page(page_title).content

# imprime o conteúdo da página da Wikipedia


dotenv.load_dotenv()  # variáveis de ambiente do arquivo .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# contexto inicial para as conversas
#contexto = "Eu tenho um gato siamês de 2 anos chamado Tom. Ele é muito brincalhão e adora perseguir bolas de papel."

# lista de frases já ditas pelo modelo
previous_sentences = set()

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
        max_tokens=20000, 
        n=1, 
        stop=None, 
        temperature=0.5,
    )
    
    message = completions.choices[0].text.strip()
    
    # dividir a mensagem em frases
    sentences = message.split(".")
    
    # selecionar apenas a primeira frase que não foi repetida anteriormente
    unique_sentence = ""
    for sentence in sentences:
        if sentence.strip() != "" and sentence not in previous_sentences:
            unique_sentence = sentence
            previous_sentences.add(sentence)
            break
    
    return unique_sentence


def enviar_pergunta():
    # obtém a pergunta digitada pelo usuário
    pergunta = entrada.get()
    
    # limpa a entrada
    entrada.delete(0, tk.END)
    
    # chama a função chatgpt para obter a resposta
    resposta = chatgpt(contexto, pergunta)
    
    # adiciona a resposta à janela de conversa
    conversa.config(state=tk.NORMAL)
    conversa.insert(tk.END, f'Usuário: {pergunta}\n')
    conversa.insert(tk.END, f'ChatGPT: {resposta}\n\n\n')
    conversa.config(state=tk.DISABLED)
    
def limpar_conversa():
    # limpa a janela de conversa
    conversa.config(state=tk.NORMAL)
    conversa.delete('1.0', tk.END)
    conversa.config(state=tk.DISABLED)


# cria a janela principal
janela = tk.Tk()
janela.title("Chat com ChatGPT")
janela.geometry("700x500")

# cria a área de conversa
conversa = tk.Text(janela, state=tk.DISABLED)
conversa.pack(fill=tk.BOTH, expand=True)

# cria a barra de rolagem para a área de conversa
scrollbar = tk.Scrollbar(conversa)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
conversa.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=conversa.yview)

# cria a área de entrada
entrada = tk.Entry(janela)
entrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# cria o botão de enviar pergunta
enviar = tk.Button(janela, text="Enviar", command=enviar_pergunta)
enviar.pack(side=tk.RIGHT)

# cria o botão de limpar a conversa
limpar = tk.Button(janela, text="Limpar Conversa", command=limpar_conversa)
limpar.pack(side=tk.BOTTOM)

# inicia o loop principal da interface
janela.mainloop()
