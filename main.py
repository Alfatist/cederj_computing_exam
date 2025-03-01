from views.admin.authAdminView import AuthAdminView
from views.user.accessAccountView import AccessAccountView
from views.user.accessingAccountView import AccessingAccountView
from views.user.authView import AuthView
from views.user.createAccountView import CreateAccountView
from views.user.createView import CreateView
from views.viewModel import ViewModel

class __mainController:
  '''cada view retorna, obrigatoriamente, ou uma lista contendo [keyValue, arguments] ou None. Se for None, ele retorna para o logout.'''
  keyValue:any
  arguments:any
  isToPopExitTutorial:bool

  def __init__(self, keyValue = None, arguments = None):
    self.keyValue, self.arguments, self.isToPopExitTutorial = keyValue, arguments, True

  def popExitTutorialIfNeed(self):
    if(self.isToPopExitTutorial): print("\nLembre-se! Você pode sempre voltar a tela inicial digitando '0'")
    self.isToPopExitTutorial = False
  
  def resetValues(self):
    self.isToPopExitTutorial, self.keyValue, self.arguments = True, None, None
    
  def executeView(self, view: ViewModel):
    try:
      view = view(self.arguments)
      result = view.call()
      if(result == None): self.keyValue = result
      else: self.keyValue, self.arguments = result
    except Exception as e:
      print("Pedimos que se logue novamente. Pedimos desculpas pela inconveniência.")
      
      self.keyValue = None


controller = __mainController()

def getKeyValue() -> str: return controller.keyValue
def arguments() -> str: return controller.arguments


while(True):
  if(getKeyValue() == None ): 
    controller.resetValues()
    initialResult = input("\n\n\n\n\n\n\n\n\n===================\n\n    CEDERJ BANK\n\n===================\nEntre (1) | Cadastre-se (2) ")
    controller.keyValue = initialResult
    if(not (initialResult == "1" or initialResult == "2" or initialResult == "admin")): 
      controller.keyValue = None
      print("Valor inválido")

  match getKeyValue():
    
    case "1": controller.executeView(AuthView)
      
    case "2": controller.executeView(CreateView)
      
    case "3":
      controller.popExitTutorialIfNeed()
      controller.executeView(AccessAccountView)

    case "4": controller.executeView(CreateAccountView)
    
    case "5": controller.executeView(AccessingAccountView)

    case "admin": controller.executeView(AuthAdminView) # deve retornar -1
    
    case None: continue


    case _:
      print("Parabéns. Esta parte do sistema ainda não está pronta.")
      break

