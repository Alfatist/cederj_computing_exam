from core.either.left import Left
from model.createAccountsJsonRepository import CreateCurrentAccountJsonRepository, CreateSavingAccountJsonRepository
from model.getAvailableAccountsJsonRepository import getAccountById, GetAvailableAccountsJsonRepository
from core.either.either import Either
from core.either.right import Right




class CreateAccountController(object):
  __name:str
  def __init__(self, name): self.__name = name
  def getName(self): return self.__name


  def createCurrentAccount(self) -> bool:
    if(type(CreateCurrentAccountJsonRepository(self.__name)) == Right): return True
    return False

  
  def createSavingAccount(self) -> bool:
    if(type(CreateSavingAccountJsonRepository(self.__name)) == Right): return True
    return False
  