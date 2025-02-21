from view.accessAccountView import AccessAccountView
from view.authView import AuthView
from view.createView import CreateView

class __mainController:
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
    

controller = __mainController()

def getKeyValue() -> str: return controller.keyValue
def arguments() -> str: return controller.arguments


while(True):
  if(getKeyValue() == None ): 
    controller.resetValues()
    controller.keyValue = input("\n\n===================\n\n    CEDERJ BANK\n\n===================\n\nSign in (1) | Sign up (2) ")
  match getKeyValue():
    case "1":
      authView = AuthView()
      result = authView.call()
      if(result == None): controller.keyValue = result
      else: controller.keyValue, controller.arguments = result
      
    case "2":
      createView = CreateView()
      result = createView.call()
      if(result == None): controller.keyValue = result
      else: controller.keyValue, controller.arguments = result
      
    case "3":
      controller.popExitTutorialIfNeed()
      accessAccountView = AccessAccountView(controller.arguments)
      result = accessAccountView.call()
      if(result == None): controller.keyValue = result
      else: controller.keyValue, controller.arguments = result
    
    case None:
      continue

    case _:
      print("Parabéns. Esta parte do sistema ainda não está pronta.")
      break

  

