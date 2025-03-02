import sys
import os

from views.viewModel import ViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.user.authUserController import AuthUserController

class AuthView(ViewModel):
  def __init__(self, argument):
    self.isToLeave = False

  def call(self, authUserController: AuthUserController = AuthUserController(), isToNullValues = True):
    self.isToLeave = False
    
    if(isToNullValues): authUserController = AuthUserController()

    if(authUserController.getName() == None ): authUserController.setName(self.inputView("Insira os dados abaixo. Caso queira retornar, basta digitar '0'\n\nlogin: "))
    if(authUserController.getpassword() == None): authUserController.setPassword(self.inputView("senha: "))
    if(self.isToLeave): return None
    result = authUserController.auth()
    
    match result:
      case -1: return self.returnView(["3", authUserController.getName()])
      case 1:
        print("Desculpe, não conseguimos encontrar a conta ") 
        return self.returnView(self.call)
      case 2: 
        password = self.inputView("Senha inválida. Por favor digite novamente ou '-1' para voltar: ")
        if(password == "-1"): return self.returnView(self.call)
        return self.call(AuthUserController(name=authUserController.getName(), password=password ), isToNullValues=False)
      case _:
        print("Desculpe, tivemos um erro interno. Tente novamente: ")
        return self.returnView(self.call)
