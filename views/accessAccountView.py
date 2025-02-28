import sys
import os

from controllers.accessAccountController import AccessAccountController
from controllers.createUserController import CreateUserController
from views.viewModel import ViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class AccessAccountView(ViewModel):
  isToLeave:bool = False
  holderName: str
  accessAccountController: AccessAccountController

  def __init__(self, holderName):
    self.accessAccountController, self.holderName = AccessAccountController(holderName), holderName

  def call(self):
    self.isToLeave = False
    accountsList = self.accessAccountController.getAvailableAccounts()
    if(accountsList == None or accountsList == []): 
      print("Parece que você ainda não tem uma conta. Vamos começar?")
      return self.returnView(["4", self.holderName])
    
    
    result = self.inputView(f"\n\n\n\n\n\n\n\n\n\n\n===\n\n{str.join(" | ", accountsList)}\n\n===\n\nPara acessar uma das contas acima, digite seu id. Para criar uma, digite 'criar':\n\n")
    if(result.lower() == "criar"): return self.returnView(["4", self.holderName])
    resultIsValid = self.accessAccountController.checkAccountExistById(result)

    match resultIsValid:
      case True: return self.returnView(["5", f"{result};{self.holderName}"])
      case False:
        if(result != self.exitValue): print("Opção Inválida.\n") 
        return self.returnView(self.call)
      case _:
        print("Desculpe, tivemos um erro interno. Tente novamente: ")
        return self.returnView(self.call)

