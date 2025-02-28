from model.getAvailableAccountsJsonRepository import getAccountById, GetAvailableAccountsJsonRepository




class AccessAccountController(object):
  __name:str
  __availableAccounts:list
  def getName(self): return self.__name

  def getAvailableAccounts(self):
    either = GetAvailableAccountsJsonRepository(self.__name)
    self.__availableAccounts = either.result
    if(self.__availableAccounts == None or self.__availableAccounts == []): return []
    return list(map(getAccountById, self.__availableAccounts))


  def __init__(self, name):
    self.__name = name
  
  def checkAccountExistById(self, idAccount) -> bool:
    try: 
      self.__availableAccounts.index(int(idAccount))
      return True
    except: return False
  