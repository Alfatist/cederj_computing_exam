import sys
import os

from controllers.user.createAccountController import CreateAccountController
from views.viewModel import ViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class CreateAccountView(ViewModel):
  isToLeave:bool = False
  holderName: str
  createAccountController: CreateAccountController

  def __init__(self, holderName):
    super().__init__()
    self.createAccountController, self.holderName = CreateAccountController(holderName), holderName

  def call(self):
    
    accountTypeChoose = self.inputView("\nCaso queira criar uma conta corrente, digite '1'. Caso queira criar uma conta poupança, digite '2'")
    match accountTypeChoose.lower():
      case "1": 
        self.setResult(self.returnView(self.__caseCurrent()))

      case "2":
        self.setResult(self.returnView(self.__caseSaving()))

      case _:
        self.print("Opção inválida. Tente novamente.")
        
        self.setResult(self.returnView(self.call))
    return self.result


  def __caseCurrent(self):
    addressUser = self.inputView("Insira o endereço: ")
    while(addressUser == ""): addressUser = self.inputView("Por favor, insira um endereço válido: ")
    agencyUser = self.__askForAgency()
    
    
    if(self.createAccountController.createCurrentAccount(addressUser, agencyUser)): 
      self.print("Conta criada com sucesso!")
      
      return self.returnView(["5", f"{self.createAccountController.getResult()};{self.holderName}"])
    
    self.print("Desculpe, algo deu erro internamente. Por favor, tente novamente.")
    
    return self.returnView(self.call)
  
  def __caseSaving(self):
    addressUser = self.inputView("Insira o endereço: ")
    while(addressUser == ""): addressUser = self.inputView("Por favor, insira um endereço válido: ")
    agencyUser = self.__askForAgency()
    if(self.isToLeave): return self.returnView([0,0])
    if(self.createAccountController.createSavingAccount(addressUser, agencyUser)): 
      self.print("Conta criada com sucesso!")
      
      return self.returnView(["5", f"{self.createAccountController.getResult()};{self.holderName}"])
    self.print("Desculpe, algo deu erro internamente. Por favor, tente novamente.")
    
    return self.returnView(self.call)
  
  def __askForAgency(self) -> str:
    if(self.isToLeave): return self.returnView([0,0])
    agencyInput = self.inputView("Agora a agência (somente números): ")
    
    while(True):
      if(agencyInput.isnumeric() and len(agencyInput.strip()) > 0): return agencyInput
      agencyInput = self.inputView("Por favor, digite uma agência válida: ")