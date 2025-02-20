from view.authView import AuthView
from view.createView import CreateView

class __mainController:
  keyValue:any
  arguments:any
  def __init__(self, keyValue = None, arguments = None):
    self.keyValue, self.arguments = keyValue, arguments

controller = __mainController()
def keyValue() -> str: return controller.keyValue
def arguments() -> str: return controller.arguments

while(True):
  if(keyValue() == None ): controller.keyValue = input("\n\n===================\n\n    CEDERJ BANK\n\n===================\n\nSign in (1) | Sign up (2) ")
  match keyValue():
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
      
    case _:
      print("congrats. This part of the system is not implemented yet.")
      break

  

