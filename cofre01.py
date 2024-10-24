import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import wavio
import os

# Configurações de gravação e diretório protegido
SAMPLE_RATE = 44100  # Taxa de amostragem
DURATION = 2         # Duração da gravação em segundos
DIRETORIO_SEGURO = 'C:/CofreDeSenhas'  # Pasta onde as gravações serão salvas

# Dicionário para armazenar senhas e números de conta
dados_usuarios = {}

# Função para gravar áudio
def gravar_audio(tipo):
    numero_conta = entry_conta.get()
    if not numero_conta:
        messagebox.showwarning("Aviso", "Por favor, insira o número da conta.")
        return

    try:
        if not os.path.exists(DIRETORIO_SEGURO):
            os.makedirs(DIRETORIO_SEGURO)

        messagebox.showinfo("Gravando", f"Iniciando a gravação de {DURATION} segundos.")
        audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
        sd.wait()  # Esperar a gravação terminar

        if tipo == 'senha':
            arquivo_senha = os.path.join(DIRETORIO_SEGURO, f"{numero_conta}_senha.wav")
            wavio.write(arquivo_senha, audio, SAMPLE_RATE, sampwidth=2)
            messagebox.showinfo("Sucesso", "Senha gravada com sucesso.")

            # Armazenar o número da conta no dicionário
            dados_usuarios[numero_conta] = {'senha': arquivo_senha}
        elif tipo == 'confirmacao':
            arquivo_confirmacao = os.path.join(DIRETORIO_SEGURO, f"{numero_conta}_confirmacao.wav")
            wavio.write(arquivo_confirmacao, audio, SAMPLE_RATE, sampwidth=2)

            if verificar_confirmacao(dados_usuarios[numero_conta]['senha'], arquivo_confirmacao):
                messagebox.showinfo("Sucesso", "Senha confirmada com sucesso.")
            else:
                messagebox.showwarning("Erro", "A confirmação de senha falhou.")

        atualizar_lista_gravacoes()

    except sd.PortAudioError as e:
        messagebox.showerror("Erro de Áudio", f"Erro ao gravar áudio: {e}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado: {e}")

# Função para verificar a confirmação da senha
def verificar_confirmacao(arquivo_senha, arquivo_confirmacao):
    return os.path.getsize(arquivo_senha) == os.path.getsize(arquivo_confirmacao)

# Função para atualizar a lista de gravações
def atualizar_lista_gravacoes():
    try:
        if not os.path.exists(DIRETORIO_SEGURO):
            os.makedirs(DIRETORIO_SEGURO)

        lista_gravacoes.delete(0, tk.END)  # Limpar a lista
        for arquivo in os.listdir(DIRETORIO_SEGURO):
            if arquivo.endswith(".wav"):
                lista_gravacoes.insert(tk.END, arquivo)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao acessar o diretório de gravações: {e}")

# Função para recuperar senha
def recuperar_senha():
    numero_conta = entry_recuperacao.get()
    
    if not numero_conta:
        messagebox.showwarning("Aviso", "Por favor, insira o número da conta para recuperação.")
        return

    # Verifica se o número da conta existe
    if numero_conta in dados_usuarios:
        arquivo_recuperacao = dados_usuarios[numero_conta]['senha']

        if os.path.exists(arquivo_recuperacao):
            messagebox.showinfo("Sucesso", "Senha recuperada com sucesso!")
            # Aqui você pode adicionar uma funcionalidade para tocar a gravação
            sd.play(wavio.read(arquivo_recuperacao).data)  # Tocar a gravação da senha
        else:
            messagebox.showwarning("Erro", "Gravação de senha não encontrada.")
    else:
        messagebox.showwarning("Erro", "Número da conta não encontrado.")

# Função para cadastrar uma nova conta
def cadastrar_conta():
    numero_conta = entry_conta.get()
    
    if not numero_conta:
        messagebox.showwarning("Aviso", "Por favor, insira um número de conta para cadastro.")
        return

    if numero_conta in dados_usuarios:
        messagebox.showwarning("Aviso", "Número da conta já cadastrado.")
        return

    dados_usuarios[numero_conta] = {'senha': None}  # Inicializa com None até que uma senha seja gravada
    messagebox.showinfo("Sucesso", "Conta cadastrada com sucesso.")

# Criar janela principal
janela = tk.Tk()
janela.title("Cofre de Senhas com Áudio")
janela.geometry("400x600")
janela.config(bg="#f0f0f0")  # Cor de fundo

# Label e campo de entrada para o número da conta
label_conta = tk.Label(janela, text="Número da Conta:", bg="#f0f0f0", fg="#333333")
label_conta.pack(pady=10)

entry_conta = tk.Entry(janela, width=30, bg="#ffffff", fg="#000000")
entry_conta.pack(pady=5)

# Botão para cadastrar a conta
btn_cadastrar = tk.Button(janela, text="Cadastrar Conta", command=cadastrar_conta, bg="#4CAF50", fg="#ffffff")
btn_cadastrar.pack(pady=10)

# Botão para gravar senha
btn_gravar_senha = tk.Button(janela, text="Gravar Senha", command=lambda: gravar_audio('senha'), bg="#2196F3", fg="#ffffff")
btn_gravar_senha.pack(pady=10)

# Botão para confirmar senha
btn_confirmar_senha = tk.Button(janela, text="Confirmar Senha", command=lambda: gravar_audio('confirmacao'), bg="#2196F3", fg="#ffffff")
btn_confirmar_senha.pack(pady=10)

# Label e campo de entrada para o número da conta de recuperação
label_recuperacao = tk.Label(janela, text="Número da Conta para Recuperação:", bg="#f0f0f0", fg="#333333")
label_recuperacao.pack(pady=10)

entry_recuperacao = tk.Entry(janela, width=30, bg="#ffffff", fg="#000000")
entry_recuperacao.pack(pady=5)

# Botão para recuperar senha
btn_recuperar_senha = tk.Button(janela, text="Recuperar Senha", command=recuperar_senha, bg="#FF9800", fg="#ffffff")
btn_recuperar_senha.pack(pady=10)

# Lista para exibir gravações salvas
lista_gravacoes = tk.Listbox(janela, width=50, bg="#ffffff", fg="#000000")
lista_gravacoes.pack(pady=10)

# Iniciar interface
atualizar_lista_gravacoes()  # Atualiza a lista ao iniciar
janela.mainloop()
