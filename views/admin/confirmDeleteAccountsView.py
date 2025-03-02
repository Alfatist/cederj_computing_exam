import sys
import os
from turtle import right

from controllers.admin.authAdminController import AuthAdminController
from controllers.admin.confirmDeleteAccountsController import ConfirmDeleteAccountsController
from core.either.left import Left
from views.viewModel import ViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.user.authUserController import AuthUserController

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
      return self.returnView([None, None])

    deleteSolicitationsAccounts = list(deleteSolicitations.keys())
    deleteSolicitationsAccountsWithHolderName = ""
    for account in deleteSolicitationsAccounts:
      deleteSolicitationsAccountsWithHolderName += f"{account}: {deleteSolicitations[account]}\n"

    idToDelete = self.inputView(f"Estas são as contas que estão pedindo exclusão:\n\n===\n{deleteSolicitationsAccountsWithHolderName}===\n\nPara confirmar a exclusão de um, digite o id.")
    
    if(self.isToLeave): return self.returnView([0,0])
    if(deleteSolicitations.get(idToDelete) == None): 
      print("Por favor, digite uma conta válida.")
      return self.returnView(self.call())
    
    result = confirmDeleteAccountsController.deleteAccount(deleteSolicitations[account], account)

    if(type(result) == right): print("Conta deletada com sucesso!")
    else: print("Desculpe, não foi possível deletar a conta. Tente novamente.")
    
    return self.returnView(self.call())
      
        





    
    
