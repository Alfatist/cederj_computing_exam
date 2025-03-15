from usecases.discountTaxCurrentAccountJsonRepository import taxCurrentAccountsJsonRepository
from usecases.taxSpecialChecksJsonRepository import taxSpecialChecksJsonRepository
from usecases.yieldSavingAccountsJsonRepository import yieldSavingAccountsJsonRepository
from views.admin.authAdminView import AuthAdminView
from views.admin.confirmDeleteAccountsView import ConfirmDeleteAccountsView
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
    if(self.isToPopExitTutorial): print("\nLembre-se! Você pode sempre voltar a tela inicial digitando '0'\n\n")
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
      print(f"Pedimos que se logue novamente. Pedimos desculpas pela inconveniência.\nErro: {e}")
      self.keyValue = None


controller = __mainController()

def getKeyValue() -> str: return controller.keyValue
def arguments() -> str: return controller.arguments


while(True):
  taxSpecialChecksJsonRepository()
  yieldSavingAccountsJsonRepository() 
  taxCurrentAccountsJsonRepository()

  match getKeyValue():

    case None: 
      controller.resetValues()
      initialResult = input("\n\n\n\n\n\n\n\n\n\n\n\n\n\n===================\n\n    CEDERJ BANK\n\n===================\nEntre (1) | Cadastre-se (2) ")
      if(initialResult != "1" and initialResult != "2" and initialResult != "admin"): 
        print("Valor inválido")
        continue
      controller.keyValue = initialResult
      

    
    case "1": controller.executeView(AuthView)
      
    case "2": controller.executeView(CreateView)
      
    case "3":
      controller.popExitTutorialIfNeed()
      controller.executeView(AccessAccountView)

    case "4": controller.executeView(CreateAccountView)
    
    case "5": controller.executeView(AccessingAccountView)

    case "admin": controller.executeView(AuthAdminView) # deve retornar -1 e o nome do adm

    case "-1": controller.executeView(ConfirmDeleteAccountsView)
    case _:
      print("Parabéns. Esta parte do sistema ainda não está pronta.")
      break

