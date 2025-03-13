from common.helpers.verifyIfExistsInList import verifyIfExistsInList
from controllers.admin.confirmDeleteAccountsController import Left
from usecases.getAvailableAccountsJsonRepository import getAvailableAccountsJsonRepository
from usecases.getAccountByIdJsonRepository import getAccountByIdJsonRepository



class AccessAccountController(object):
  __name:str
  __availableAccounts:list
  
  def __init__(self, name): self.__name = name
  def getName(self): return self.__name

  def getAvailableAccounts(self) -> Left | list:
    either = getAvailableAccountsJsonRepository(self.__name)
    if(type(either) == Left): return either
    
    self.__availableAccounts = either
    if(self.__availableAccounts == None or self.__availableAccounts == []): return []
    return list(map(getAccountByIdJsonRepository, self.__availableAccounts))

  
  def checkAccountExistById(self, idAccount) -> bool: return verifyIfExistsInList(self.__availableAccounts, idAccount)
  