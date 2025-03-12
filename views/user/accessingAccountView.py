import sys
import os

from controllers.user.accessingAccountController import AccessingAccountController
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
    availableCheck = self.accessingAccountController.getAvailableCheck()
    valueToPay = self.accessingAccountController.getValueToPaySpecialCheck()
    if(type(valueToPay) == Left): valueToPay = 0
    print(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nVocê está acessando a conta de id {self.accessingAccountController.getAccountId()}")
    print("===")
    print(f"Saldo: {self.accessingAccountController.getBalance()}")
    print(f"Endereço: {self.accessingAccountController.getAddress()}")
    if(type(availableCheck) == float): print(f"Cheque especial disponível: {availableCheck}")
    if(valueToPay > 0): print(f"Valor a ser pago de cheque especial: {valueToPay}")
    print("===\n")
    print("Depositar (1) | Transferir (2) | Sacar (3) | Ver extrato (4) | Alterar endereço (5) | Solicitar exclusão (6) | Sair (0)")
    if(valueToPay > 0): print(f"Caso queira pagar o cheque especial, entre com 'pagar'")
    operation = self.inputView()
    match operation:
      case "1": 
        valueToAdd = self.inputView("Digite o quanto você deseja depositar (ou 'voltar' para voltar): ")
        while(True):
          if(self.isToLeave): return self.returnView([0,0])
          if(valueToAdd.lower() == "voltar"): return self.returnView(self.call)
          if(valueToAdd.isnumeric() and float(valueToAdd) > 0): break
          valueToAdd = self.inputView("Por favor, digite um número válido: ")
        result = self.accessingAccountController.addMoney(float(valueToAdd))
        
        if(type(result) == Right): print(f"\n{valueToAdd} adicionado na conta com êxito!")
        if(type(result) == Left): print("\n Algo deu errado. Por favor, repita a operação.")
        
        self.pressAnyKeyToContinue()
        return self.returnView(self.call)
      case "2":
        idAccountTotransfer = self.inputView("Digite o id da conta para a qual você quer transferir (ou 'voltar' para voltar): ")
        if(self.isToLeave): return self.returnView([0,0])
        if(idAccountTotransfer == self.accessingAccountController.getAccountId() or not self.accessingAccountController.checkAccountExist(idAccountTotransfer) or idAccountTotransfer.lower() == "voltar"): return self.returnView(self.call())
        valueToTransfer = self.inputView("Agora digite o valor a ser transferido: ")
        while(True):
          if(self.isToLeave): return self.returnView([0,0])
          if(valueToTransfer.lower() == "voltar"): return self.returnView(self.call)
          if(valueToTransfer.isnumeric()):
            valueToTransfer = float(valueToTransfer)
            if(0 < valueToTransfer < self.accessingAccountController.getBalance()): break
          valueToTransfer = self.inputView("Por favor, digite um valor válido: ")
        result = self.accessingAccountController.transferMoneyToAccount(idAccountTotransfer, float(valueToTransfer))
        if(type(result) == Right): print(f"\n{valueToTransfer} transferido para a conta {idAccountTotransfer} com êxito!")
        if(type(result) == Left): print("\n Algo deu errado. Por favor, repita a operação.")
        self.pressAnyKeyToContinue()
        return self.returnView(self.call)
      case "3":
        valueToAdd = self.inputView("Digite o quanto você deseja sacar (ou 'voltar' para voltar): ")
        while(True):
          if(self.isToLeave): return self.returnView([0,0])
          if(valueToAdd.lower() == "voltar"): return self.returnView(self.call)
          if(valueToAdd.isnumeric() and float(valueToAdd) > 0): break
          valueToAdd = self.inputView("Por favor, digite um número válido: ")
        result = self.accessingAccountController.withdrawMoney(float(valueToAdd))
        
        if(type(result) == Right): print(f"\n{valueToAdd} sacado da conta com êxito!")
        if(type(result) == Left): print("\n Algo deu errado. Por favor, repita a operação.")
        
        self.pressAnyKeyToContinue()
        return self.returnView(self.call)
      case "4":

        dateEntry = self.inputView("Selecione a partir de qual data gostaria de começar, ou insira nada para pegar todo o extrato (dd/mm/YYYY): ").strip()
        dateEnding = ""
        if(not (dateEntry == None or dateEntry == "")): dateEnding = self.inputView("Até qual data? (dd/mm/YYYY): ").strip()
        print(f"\n{self.accessingAccountController.getStatementOfAccount(dateEntry, dateEnding)}\n")
        self.pressAnyKeyToContinue()
        return self.returnView(self.call) 
      case "5": 
        resultEither = type(self.accessingAccountController.changeHolderAddress(self.inputView("Digite o novo endereço: ")))
        if(resultEither == Right): print("Endereço alterado com êxito.")
        if(resultEither == Left):  print("desculpe, não foi possível alterar o endereço.")
        self.pressAnyKeyToContinue()
        return self.returnView(self.call)
      case "6":
        confirm = self.inputView("Para confirmar a operação, digite seu nome: ")
        if(confirm != self.accessingAccountController.getName()): return self.returnView(self.call)
        result = self.accessingAccountController.orderDeleteAccount()
        if(type(result) == Right): 
          print("\n\nBeleza, sua solicitação de exclusão foi solicitada para um dos nossos adms. Agradecemos a preferência :)")
          return self.returnView([None, None])
        
        print("\nDesculpa, mas algo deu errado na solicitação. Tente novamente.\n")
        return self.returnView(self.call)
      case "pagar":
        if(type(valueToPay) == Left): print(f"Desculpa, mas não conseguimos efetuar a operação.\n{Left}\n Tente novamente.")
          
        resultPaying = self.accessingAccountController.paySpecialCheck()

        if(type(resultPaying) == Left and resultPaying.code != 13): print("Desculpe, não conseguimos pagar. Tente novamente.")
        else: print(f"{valueToPay} do cheque especial pago com sucesso!")

        self.pressAnyKeyToContinue()
        return self.returnView(self.call)
        
