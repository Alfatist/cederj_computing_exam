import sys
import os

from controllers.admin.authAdminController import AuthAdminController
from views.viewModel import ViewModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk

class AuthAdminView(ViewModel):
  def __init__(self, argument):
    super().__init__()
    

  def call(self, authAdminController: AuthAdminController = AuthAdminController(), isToNullValues = True):

    
    if(isToNullValues): authAdminController = AuthAdminController()

    if(authAdminController.getName() == None ): authAdminController.setName(self.inputView("Insira o código: "))
    result = authAdminController.auth()
    
    if(self.values == None): 
      self.setResult(None)
      return self.result
    

    match result.code:
      case -1: self.setResult(self.returnView(["-1", authAdminController.getName()]))
      case 1:
        self.print("Desculpe, não conseguimos encontrar a conta ") 
        self.setResult(self.returnView(self.call))
      case 2: 
        password = self.inputView("Senha inválida. Por favor digite novamente ou '-1' para voltar: ")
        if(password == "-1"): return self.returnView(self.call)
        self.setResult(self.call(AuthAdminController(name=authAdminController.getName(), password=password ), isToNullValues=False))
      case _:
        self.print("Desculpe, tivemos um erro interno. Tente novamente: ")
        self.setResult(self.returnView(self.call))
    self.root.mainloop()
    return self.result