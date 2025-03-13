from usecases.createCurrentAccountJsonRepository import createCurrentAccountJsonRepository
from usecases.createSavingAccountJsonRepository import createSavingAccountJsonRepository
from core.either.right import Right




class CreateAccountController(object):
  __name:str
  def __init__(self, name): self.__name = name
  def getName(self): return self.__name


  def createCurrentAccount(self, address, agency) -> bool:
    result = createCurrentAccountJsonRepository(self.__name, address, agency)
    if(type(result) == Right): return True
    return False

  
  def createSavingAccount(self, address, agency) -> bool:
    result = createSavingAccountJsonRepository(self.__name, address, agency)
    if(type(result) == Right): return True
    return False
  