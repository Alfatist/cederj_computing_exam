from usecases.createCurrentAccountJsonRepository import createCurrentAccountJsonRepository
from usecases.createSavingAccountJsonRepository import createSavingAccountJsonRepository
from core.either.right import Right
from core.either.left import Left




class CreateAccountController(object):
  __name:str
  __result:str

  def __init__(self, name): self.__name = name
  def getName(self): return self.__name
  def getResult(self): return self.__result

  def createCurrentAccount(self, address, agency) -> bool:
    result = createCurrentAccountJsonRepository(self.__name, address, agency)
    if(type(result) == Left): raise result.result
    if(type(result) == Right): 
      self.__result = result.result
      return True
    return False

  
  def createSavingAccount(self, address, agency) -> bool:
    result = createSavingAccountJsonRepository(self.__name, address, agency)
    if(type(result) == Right): 
      self.__result = result.result
      return True
    return False
  