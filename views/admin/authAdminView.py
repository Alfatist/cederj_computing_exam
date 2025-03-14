import sys
import os

from controllers.admin.authAdminController import AuthAdminController
from views.viewModel import ViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.user.authUserController import AuthUserController

class AuthAdminView(ViewModel):
  def __init__(self, argument):
    self.isToLeave = False

  def call(self, authAdminController: AuthAdminController = AuthAdminController(), isToNullValues = True):

    self.isToLeave = False
    
    if(isToNullValues): authAdminController = AuthAdminController()

    if(authAdminController.getName() == None ): authAdminController.setName(self.inputView("Insira os dados abaixo. Caso queira retornar, basta digitar '0'\n\nlogin: "))
    if(authAdminController.getpassword() == None): authAdminController.setPassword(self.inputView("senha: "))
    if(self.isToLeave): return None
    result = authAdminController.auth()
    
    match result.code:
      case -1: return self.returnView(["-1", authAdminController.getName()])
      case 1:
        print("Desculpe, não conseguimos encontrar a conta ") 
        return self.returnView(self.call)
      case 2: 
        password = self.inputView("Senha inválida. Por favor digite novamente ou '-1' para voltar: ")
        if(password == "-1"): return self.returnView(self.call)
        return self.call(AuthAdminController(name=authAdminController.getName(), password=password ), isToNullValues=False)
      case _:
        print("Desculpe, tivemos um erro interno. Tente novamente: ")
        return self.returnView(self.call)
