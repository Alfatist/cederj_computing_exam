import sys
import os

from controllers.user.accessingAccountController import AccessingAccountController
from core.either.left import Left
from core.either.right import Right

from usecases.getAccountJsonRepository import getAccountJsonRepository
from views.viewModel import ViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox

class AccessingAccountView(ViewModel):
  isToLeave:bool = False
  holderName: str
  accountToAccess:str
  accessingAccountController: AccessingAccountController

  def __init__(self, arguments: str):
    super().__init__()
    argumentList = arguments.split(";")
    self.accountToAccess, self.holderName = argumentList[0], argumentList[1]
    self.accessingAccountController, self.holderName = AccessingAccountController(self.holderName, self.accountToAccess), self.holderName

  def call(self, arguments = ""):
    self.isToLeave = False
    availableCheck = self.accessingAccountController.getAvailableCheck()
    valueToPay = self.accessingAccountController.getValueToPaySpecialCheck()
    solicitationStatus = self.accessingAccountController.getSolicitationStatus()
    agency = getAccountJsonRepository(self.accessingAccountController.getAccountId())["agency"]
    
    if(type(valueToPay) == Left): valueToPay = 0

    self.root = tk.Tk()
    self.root.title("CEDERJ BANK")

    tk.Label(self.root, text=f"Você está acessando a conta de id {self.accessingAccountController.getAccountId()}\nSaldo: {self.accessingAccountController.getBalance()}\nEndereço: {self.accessingAccountController.getAddress()}\nAgência: {agency}", font=("Arial", 11)).pack(pady=5, padx=5)
    
    if(type(availableCheck) == float): tk.Label(self.root, text=f"Cheque especial disponível: {availableCheck}", font=("Arial", 11)).pack(pady=5, padx=5)
    if(type(solicitationStatus) != Left and solicitationStatus != None ): tk.Label(self.root, text=f"Status da solicitação de exclusão de conta: {solicitationStatus}", font=("Arial", 11)).pack(pady=5, padx=5)

    if(valueToPay > 0): tk.Label(self.root, text=f"Valor a ser pago de cheque especial: {valueToPay}", font=("Arial", 11)).pack(pady=20, padx=5)
    
    tk.Button(self.root, text="Depositar", width=20, command=lambda: self.setResult("1")).pack(pady=5)
    tk.Button(self.root, text="Transferir", width=20, command=lambda: self.setResult("2")).pack(pady=5)
    tk.Button(self.root, text="Sacar", width=20, command=lambda: self.setResult("3")).pack(pady=5)
    tk.Button(self.root, text="Ver extrato", width=20, command=lambda: self.setResult("4")).pack(pady=5)
    tk.Button(self.root, text="Alterar Endereço", width=20, command=lambda: self.setResult("5")).pack(pady=5)
    tk.Button(self.root, text="Solicitar Exclusão", width=20, command=lambda: self.setResult("6")).pack(pady=5)
    tk.Button(self.root, text="Pagar cheque especial", width=20, command=lambda: self.setResult("pagar")).pack(pady=5)

    self.root.mainloop()

    match self.result:
      case "1": 
        while(True):
          self.askValue("Digite o quanto você deseja depositar: ")
          if(self.values.isnumeric() and float(self.values) > 0): break
          
          messagebox.showwarning("Por favor", "Digite um número válido")

        result = self.accessingAccountController.addMoney(float(self.values))
        
        if(type(result) == Right): messagebox.showinfo("Sucesso", f"\n{self.values} adicionado na conta com êxito!")
        if(type(result) == Left): messagebox.showerror("Erro", "\n Algo deu errado. Por favor, repita a operação.")
        
        self.setResult(self.returnView(self.call))
      
      # TODO
      case "2":
        
        self.askValue("Digite o id da conta para a qual você deseja transferir: ")

        idAccountTotransfer = self.values

        if(idAccountTotransfer == self.accessingAccountController.getAccountId() or not self.accessingAccountController.checkAccountExist(idAccountTotransfer) or idAccountTotransfer.lower() == "voltar"): 
          messagebox.showwarning("Atenção", "Você não pode transferir para si mesmo ou para uma conta inexistente.")
          self.setResult(self.returnView(self.call))


        while(True):
          self.askValue("Agora digite o valor a ser transferido: ")
          valueToTransfer = self.values

          if(valueToTransfer.isnumeric()):
            valueToTransfer = float(valueToTransfer)
            actualBalance = self.accessingAccountController.getActualBalance()
            if(0 < valueToTransfer <= actualBalance): break
            messagebox.showerror("Atenção", "Você não pode transferir um valor maior do que o saldo atual.")
            continue
          messagebox.showwarning("Atenção", "Digite um valor válido.")

        result = self.accessingAccountController.transferMoneyToAccount(idAccountTotransfer, float(valueToTransfer))
        if(type(result) == Right): messagebox.showinfo("Sucesso", f"\n{valueToTransfer} transferido para a conta {idAccountTotransfer} com êxito!")
        if(type(result) == Left): messagebox.showinfo("Erro", "\n Algo deu errado. Por favor, repita a operação.")
        self.setResult(self.returnView(self.call))
        
      case "3":
        
        while(True):
          self.askValue("Digite o quanto você deseja sacar: ")
          valueToAdd = self.values

          if(valueToAdd.isnumeric() and float(valueToAdd) > 0): break
          messagebox.showwarning("Atenção", "Digite um número válido")
        result = self.accessingAccountController.withdrawMoney(float(valueToAdd))
        
        if(type(result) == Right): self.print(f"\n{valueToAdd} sacado da conta com êxito!")
        if(type(result) == Left): 
          match result.code:
            case 9: self.print("Não há dinheiro o suficiente para a operação.")
            case 11: self.print("Não há dinheiro o suficiente para a operação.")
            case _: self.print("Desculpe, não conseguimos efetuar a operação.")
        
        self.setResult(self.returnView(self.call))
      case "4":

        dateEntry = self.inputView("Selecione a partir de qual data gostaria de começar, ou insira nada para pegar todo o extrato (dd/mm/YYYY): ").strip()
        dateEnding = ""
        if(not (dateEntry == None or dateEntry == "")): dateEnding = self.inputView("Até qual data? (dd/mm/YYYY): ").strip()
        self.print(f"\n{self.accessingAccountController.getStatementOfAccount(dateEntry, dateEnding)}\n")
        self.setResult(self.returnView(self.call))
      case "5": 
        resultEither = type(self.accessingAccountController.changeHolderAddress(self.inputView("Digite o novo endereço: ")))
        if(resultEither == Right): self.print("Endereço alterado com êxito.")
        if(resultEither == Left):  self.print("desculpe, não foi possível alterar o endereço.")
        
        self.setResult(self.returnView(self.call))
      case "6":
        confirm = self.inputView("Para confirmar a operação, digite seu nome: ")
        if(confirm != self.accessingAccountController.getName()): 
          self.print("Valor errado. Tente novamente.")
          self.setResult(self.returnView(self.call))
        result = self.accessingAccountController.orderDeleteAccount()
        if(type(result) == Right): 
          self.print("\n\nBeleza, sua solicitação de exclusão foi solicitada para um dos nossos adms. Agradecemos a preferência :)")
          self.setResult(self.returnView([None, None]))
          return
        
        self.print("\nDesculpa, mas algo deu errado na solicitação. Tente novamente.\n")
        self.setResult(self.returnView(self.call))
      case "pagar":
        if(type(valueToPay) == Left): self.print(f"Desculpa, mas não conseguimos efetuar a operação.\n{Left}\n Tente novamente.")
          
        resultPaying = self.accessingAccountController.paySpecialCheck()

        if(type(resultPaying) == Left): 
          match resultPaying.code:
            case 11: self.print("Não há dinheiro o suficiente para a operação.")
            case 13: self.print("Não há valor para pagar de cheque especial.")
            case _: self.print("Desculpe, ocorreu um erro interno. Tente novamente.")
        else: self.print(f"{valueToPay} do cheque especial pago com sucesso!")

        self.setResult(self.returnView(self.call))
    return self.result
        
