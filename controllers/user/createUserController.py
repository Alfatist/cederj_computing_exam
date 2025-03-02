from core.either.either import Either
from core.either.right import Right
from usecases.createUserJsonRepository import CreateUserJsonRepository


class CreateUserController(object):
  __name:str
  __password:str
  
  def getName(self): return self.__name
  def getpassword(self): return self.__password
  
  def setName(self, name:str):
    self.__name = name
  
  def setPassword(self, password:str):
    self.__password = password

  def __init__(self, name = None, password = None):
    self.__name, self.__password = name, password

  def create(self) -> Either:
    either = CreateUserJsonRepository(self.__name, self.__password)
    if(type(either) == Right):
      return -1
    return either.result  