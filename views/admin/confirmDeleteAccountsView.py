import sys
import os

from controllers.admin.authAdminController import AuthAdminController
from controllers.admin.confirmDeleteAccountsController import ConfirmDeleteAccountsController
from core.either.left import Left
from core.either.right import Right
from views.viewModel import ViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ConfirmDeleteAccountsView(ViewModel):
  def __init__(self, argument):
    print(f"Seja bem vindo a visualização de ADM, {argument}")
    self.isToLeave = False

  def call(self, confirmDeleteAccountsController: ConfirmDeleteAccountsController = ConfirmDeleteAccountsController(), isToNullValues = True):

    self.isToLeave = False
    
    deleteSolicitations = confirmDeleteAccountsController.getDeleteSolicitations()

    if(type(deleteSolicitations) == Left):
      print("Tivemos um erro ao tentar pegar as solicitações de exclusão de contas. Por favor, tente novamente.")
      self.returnView([None, None])

    if(deleteSolicitations == {} or deleteSolicitations == None):
      print("Parece que não há contas pedindo exclusão.")
      self.pressAnyKeyToContinue()
      return self.returnView([None, None])

    deleteSolicitationsAccounts = list(deleteSolicitations.keys())
    deleteSolicitationsAccountsWithHolderName = ""
    for account in deleteSolicitationsAccounts:
      deleteSolicitationsAccountsWithHolderName += f"{account}: {deleteSolicitations[account]}\n"

    idToDelete = self.inputView(f"Estas são as contas que estão pedindo exclusão:\n\n===\n{deleteSolicitationsAccountsWithHolderName}===\n\nPara confirmar a exclusão de um, digite o id.\nPara rejeitar, digite o id precedido de um '!', como !1:\n\n")
    
    if(self.isToLeave): return self.returnView([0,0])
    if(deleteSolicitations.get(idToDelete.replace("!", "", 1)) == None): 
      print("Por favor, digite uma conta válida.")
      return self.returnView(self.call)
    
    if(idToDelete[0] == "!"):
      idToDelete = idToDelete.replace("!", "")
      result = confirmDeleteAccountsController.denyDeleteAccount(idToDelete)
      if(type(result) == Right): print(f"Solicitação de exclusão da conta {idToDelete} negada com sucesso!")
      else: print("Desculpe, não foi possível deletar a conta. Tente novamente.")  
    
    else:
      result = confirmDeleteAccountsController.deleteAccount(deleteSolicitations[idToDelete], idToDelete)
      if(type(result) == Right): print(f"Conta {idToDelete} deletada com sucesso!")
      else: print("Desculpe, não foi possível deletar a conta. Tente novamente.")

    self.pressAnyKeyToContinue()
    return self.returnView(self.call)
      
        





    
    
