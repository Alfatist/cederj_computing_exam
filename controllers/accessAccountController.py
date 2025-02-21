from core.either.left import Left
from model.getAvailableAccountsJsonRepository import getAccountById, GetAvailableAccountsJsonRepository
from core.either.either import Either
from core.either.right import Right




class AccessAccountController(object):
  __name:str
  __availableAccounts:list
  def getName(self): return self.__name

  def getAvailableAccounts(self):
    either = GetAvailableAccountsJsonRepository(self.__name)
    self.__availableAccounts = either.result
    return list(map(getAccountById, self.__availableAccounts))


  def __init__(self, name):
    self.__name = name
  
  def checkAccountExistById(self, idAccount) -> bool:
    try: 
      self.__availableAccounts.index(int(idAccount))
      return True
    except: return False
  

  def enterAccount(self, name):
    raise NotImplementedError
  
  def createAccount(self, name):
    raise NotImplementedError
  