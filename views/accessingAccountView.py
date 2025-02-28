import sys
import os

from controllers.accessingAccountController import AccessingAccountController
from core.either.left import Left
from core.either.right import Right

from views.viewModel import ViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class AccessingAccountView(ViewModel):
  isToLeave:bool = False
  holderName: str
  accountToAccess:str
  accessingAccountController: AccessingAccountController

  def __init__(self, arguments: str):
    argumentList = arguments.split(";")
    self.accountToAccess, self.holderName = argumentList[0], argumentList[1]
    self.accessingAccountController, self.holderName = AccessingAccountController(self.holderName, self.accountToAccess), self.holderName

  def call(self):
    self.isToLeave = False
    print(f"\n===\nVocê está acessando a conta de id {self.accessingAccountController.getAccountId()}\nSaldo:{self.accessingAccountController.getBalance()}\nEndereço:{self.accessingAccountController.getAddress()}\n===\n\n")
    operation = self.inputView("Depositar (1) | Transferir (2) | Ver extrato (3) | Alterar endereço (4) | Solicitar exclusão (5)\n")

    
    match operation:
      case "1": 
        valueToAdd = self.inputView("Digite o quanto você deseja depositar (ou 'voltar' para voltar): ")
        while(True):
          if(valueToAdd.lower() == "voltar"): return self.returnView(self.call())
          if(valueToAdd.isnumeric() and float(valueToAdd) > 0): break
          valueToAdd = self.inputView("Por favor, digite um número válido: ")
        result = self.accessingAccountController.addMoney(float(valueToAdd))
        
        if(type(result) == Right): print(f"\n{valueToAdd} adicionado na conta com êxito!")
        if(type(result) == Left): print("\n Algo deu errado. Por favor, repita a operação.")
        return self.returnView(self.call())
      case "2":
        idAccountTotransfer = self.inputView("Digite o id da conta para a qual você quer transferir (ou 'voltar' para voltar): ")
        if(idAccountTotransfer == self.accessingAccountController.getAccountId() or not self.accessingAccountController.checkAccountExist(idAccountTotransfer) or idAccountTotransfer.lower() == "voltar"): return self.returnView(self.call())
        valueToTransfer = self.inputView("Agora digite o valor a ser transferido: ")
        while(True):
          if(valueToTransfer.lower() == "voltar"): return self.returnView(self.call())
          if(valueToTransfer.isnumeric()):
            valueToTransfer = float(valueToTransfer)
            if(0 < valueToTransfer < self.accessingAccountController.getBalance()): break
          valueToTransfer = self.inputView("Por favor, digite um valor válido: ")
        result = self.accessingAccountController.transferMoneyToAccount(idAccountTotransfer, float(valueToTransfer))
        if(type(result) == Right): print(f"\n{valueToTransfer} transferido para a conta {idAccountTotransfer} com êxito!")
        if(type(result) == Left): print("\n Algo deu errado. Por favor, repita a operação.")
        return self.returnView(self.call())
      case "3":
        print(f"\n{self.accessingAccountController.getStatementOfAccount()}\n")
        return self.returnView(self.call()) 
        
  