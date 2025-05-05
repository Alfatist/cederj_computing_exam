import sys
import os
from core.either.left import Left

from controllers.user.accessAccountController import AccessAccountController
from controllers.user.createUserController import CreateUserController
from views.viewModel import ViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox


class AccessAccountView(ViewModel):
  isToLeave:bool = False
  holderName: str
  accessAccountController: AccessAccountController

  def __init__(self, holderName):
    super().__init__()
    self.accessAccountController, self.holderName = AccessAccountController(holderName), holderName

  def call(self):
    self.isToLeave = False
    accountsList = self.accessAccountController.getAvailableAccounts()

    self.root = tk.Tk()
    self.root.title("Acessar Conta - CEDERJ BANK")

    if(type(accountsList) == Left): 
      messagebox.showerror("Erro, não conseguimos acessar as contas possuída.")
      self.root.destroy()
      return self.returnView([None, None])
    
    if(accountsList == None or accountsList == []): 
      messagebox.showwarning("Aviso", "não conseguimos acessar as contas possuída.")
      self.create_account()
    
    tk.Label(self.root, text="Escolha uma conta:", font=("Arial", 11)).pack(pady=5)
    for i in accountsList:
      tk.Button(self.root, text=i, width=20, command=lambda: self.on_select(i[-2])).pack(pady=5)
    tk.Button(self.root, text="Criar", width=20, command=self.create_account).pack(pady=5)
    self.root.mainloop()
    return self.result


  def on_select(self, value):
    self.setResult(self.returnView(["5", f"{value};{self.holderName}"]))
    
  
  def create_account(self):
    self.setResult(self.returnView(["4", self.holderName]))
    
    

  # def 
  #   match resultIsValid:
  #     case True: return self.returnView(["5", f"{result};{self.holderName}"])
  #     case False:
  #       if(result != self.exitValue): print("Opção Inválida.\n") 
  #       self.pressAnyKeyToContinue()
  #       return self.returnView(self.call)
  #     case _:
  #       print("Desculpe, tivemos um erro interno. Tente novamente: ")
  #       self.pressAnyKeyToContinue()
  #       return self.returnView(self.call)

