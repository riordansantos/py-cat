import openai, dotenv, os
import tkinter as tk
from tkinter import scrolledtext, font, ttk
from PIL import Image, ImageTk

dotenv.load_dotenv()
# Initialize the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_resposta(messages):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=messages,
        max_tokens=1024,
        temperature=0.5
    )
    return [response.choices[0].text, response.usage]

mensagens = "Olá! Digite sua mensagem relacionada a gatos abaixo e pressione ENTER para enviar.\n"

def enviar_mensagem():
    global mensagens
    keywords = ["gato", "gata", "gatas", "gatos", "felino", "felinos", "miau", "miado", "dele", "dela", "deles", "delas", "ele", "ela", "eles", "elas", "olá", "oi"]
    question = entrada.get()

    if question == "":
        return

    if any(word in question.lower() for word in keywords):
        mensagens += "\nVocê: " + question + "\n"
        answer = gerar_resposta(mensagens)
        mensagens += answer[0] + "\n"
    else:
        mensagens += "\nDesculpe, mas as perguntas devem ser relacionadas a gatos. Tente novamente!\n"

    area_texto.delete('1.0', tk.END)
    area_texto.insert(tk.END, mensagens)
    entrada.delete(0, tk.END)

# Interface
janela = tk.Tk()
janela.title("ChatGPT - Gatos")
janela.geometry("700x650")
janela.configure(bg='#2d3142')
fonte = tk.font.Font(family="Tahoma", size=10)

# Cores
cor_fundo = "#2d3142"
cor_borda = "#000000"
cor_botao = "#f86624"

# Label com o texto "PyCat"
label = tk.Label(janela, text="PyCat")
label.configure(font=("Tahoma", 20), fg="white", bg="#2d3142")
label.pack(pady=10)

# Imagem do gato
img = Image.open("cat.png")
img = img.resize((50, 50), Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(img)

# Cria o label com a imagem
img_label = tk.Label(janela, image=img, padx=5, pady=5)
img_label.pack(side=tk.TOP)

# Área de texto
area_texto = scrolledtext.ScrolledText(janela, width=75, height=25)
area_texto.pack(padx=1, pady=5)
area_texto.insert(tk.END, mensagens)
area_texto.configure(background=cor_fundo, padx=10, pady=10)

# Entrada de texto
# Cria um estilo personalizado com o border radius
style = ttk.Style()
style.configure('RoundedEntry.TEntry', borderwidth=2, relief='raised', 
                background='#fff', foreground='#000', 
                highlightthickness=1, 
                bordercolor='#000', 
                focuscolor='#000', 
                padding=5, 
                roundness=15,
                font=fonte)

# Cria a caixa de texto com o estilo personalizado
entrada = ttk.Entry(janela, width=78, style='RoundedEntry.TEntry')
entrada.pack(padx=10, pady=10)
entrada.bind('<Return>', lambda event: enviar_mensagem())

# Botão
class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius, bg_color, fg_color, text="", command=None):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bd=0, bg=bg_color)

        self.corner_radius = corner_radius

        # Cria um retângulo com bordas arredondadas
        self.create_rounded_rectangle(0, 0, width, height, radius=corner_radius, fill=bg_color, outline=fg_color)

        # Adiciona o texto ao botão
        self.create_text(width // 2, height // 2, text=text, fill=fg_color, font=("Arial", 12))

        # Adiciona o evento de clique ao botão
        if command:
            self.bind("<Button-1>", lambda event: command())

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1,
                  x1 + radius, y1]

        return self.create_polygon(points, **kwargs, smooth=True)

# Criando o botão personalizado
botao = RoundedButton(janela, width=100, height=30, corner_radius=20, bg_color="#f86624", fg_color="#FFFFFF", text="Enviar", command=enviar_mensagem)
botao.pack(padx=10, pady=10)

area_texto.configure(font=fonte, foreground="#fff")



janela.mainloop()
