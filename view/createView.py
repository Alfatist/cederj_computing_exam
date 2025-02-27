import sys
import os

from controllers.createUserController import CreateUserController
from view.viewModel import ViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class CreateView(ViewModel):
  def __init__(self, argument):
    self.isToLeave = False

  def call(self, createUserController: CreateUserController = CreateUserController(), isToNullValues = True):
    if(isToNullValues): createUserController = CreateUserController()
    self.isToLeave = False
    
    if(createUserController.getName() == None ): createUserController.setName(self.inputView("Insira os dados abaixo para realizar seu cadastro. Caso queira retornar, basta digitar '0'\n\nPrimeiro Nome: "))
    if(createUserController.getpassword() == None): createUserController.setPassword(self.inputView("Senha: "))
    if(self.isToLeave): return None
    result = createUserController.create()
    
    match result:
      case -1: return self.returnView(["3", createUserController.getName()])
      case 3:
        print("Este nome já está em uso. Tente outro. ")  
        return self.returnView(self.call)
      case 4: 
        print("Senha fraca. Por favor, insira ao mínimo 8 caracteres. ")
        return self.returnView(self.call(CreateUserController(name=createUserController.getName()), isToNullValues=False))
      case _:
        print("Desculpe, tivemos um erro interno. Por favor, tente novamente: ")
        return self.returnView(self.call)
