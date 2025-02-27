import sys
import os

from controllers.accessAccountController import AccessAccountController
from controllers.createAccountController import CreateAccountController
from controllers.createUserController import CreateUserController
from view.viewModel import ViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class CreateAccountView(ViewModel):
  isToLeave:bool = False
  holderName: str
  createAccountController: CreateAccountController

  def __init__(self, holderName):
    self.createAccountController, self.holderName = CreateAccountController(holderName), holderName

  def call(self):
    self.isToLeave = False
    accountTypeChoose = self.inputView("\nCaso queira criar uma conta corrente, digite '1'. Caso queira criar uma conta poupança, digite '2'\nCaso queira voltar, digite 'voltar'\n\n")
    
    match accountTypeChoose.lower():
      case "voltar": return self.returnView(["3", self.holderName])
      case "1": 
        if(self.createAccountController.createCurrentAccount()): 
          print("Conta criada com sucesso!")
          return self.returnView(["3", self.holderName])
        print("Desculpe, algo deu erro internamente. Por favor, tente novamente.")
        return self.returnView(self.call())
      case "2":
        if(self.createAccountController.createSavingAccount()): 
          print("Conta criada com sucesso!")
          return self.returnView(["3", self.holderName])
        print("Desculpe, algo deu erro internamente. Por favor, tente novamente.")
        return self.returnView(self.call())


