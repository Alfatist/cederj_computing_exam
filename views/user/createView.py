import sys
import os

from controllers.user.createUserController import CreateUserController
from views.viewModel import ViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox

class CreateView(ViewModel):
  def __init__(self, argument):
    super().__init__()
    

  def call(self, createUserController: CreateUserController = CreateUserController(), isToNullValues = True):
    if(isToNullValues): self.createUserController = CreateUserController()
    self.isToLeave = False
    
    self.root = tk.Tk()
    
    self.root.title("Criar Conta - CEDERJ BANK")

    tk.Label(self.root, text="Insira seus dados para login", font=("Arial", 12)).pack(pady=10)
    tk.Label(self.root, text="Insira o primeiro nome:").pack()
    self.login_entry = tk.Entry(self.root)
    self.login_entry.pack()

    tk.Label(self.root, text="Senha:").pack()
    self.password_entry = tk.Entry(self.root, show="*")
    self.password_entry.pack()

    self.login_button = tk.Button(self.root, text="Entrar", command=lambda:(
                                  self.createUserController.setName(self.login_entry.get()),
                                  self.createUserController.setPassword(self.password_entry.get()),
                                  self.handle_auth(self.createUserController.create())
                                  ))
    self.login_button.pack(pady=10)
    self.root.mainloop()
    return self.result

  def handle_auth(self, result):
    match result:
      case -1: 
        messagebox.showinfo("Sucesso!", "Cadastro realizado com sucesso!")
        self.root.destroy()
        
        self.result = ["4", self.createUserController.getName()]
      case 3:
        messagebox.showerror("Erro", "Este nome já está em uso. Tente outro.")
        self.root.destroy()
        self.result = self.call()
      case 4: 
        messagebox.showerror("Erro", "Senha muito fraca. Por favor, insira ao mínimo 8 caracteres.")
        self.root.destroy()
        self.result = self.call(CreateUserController(name=self.createUserController.getName()), isToNullValues=False)
      case _:
        messagebox.showerror("Erro", "Desculpe, tivemos um erro interno. Por favor, tente novamente.")
        self.result = self.call()
        self.root.destroy()