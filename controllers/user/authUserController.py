from core.either.either import Either
from core.either.right import Right
from usecases.authUserJsonRepository import AuthUserJsonRepository


class AuthUserController(object):
  __name:str
  __password:str
  __resultAccount:str
  
  def getName(self): return self.__name
  def getpassword(self): return self.__password
  def getResultAccount(self): return self.__resultAccount

  
  def setName(self, name:str):
    self.__name = name
  
  def setPassword(self, password:str):
    self.__password = password

  def __init__(self, name = None, password = None):
    self.__name, self.__password = name, password

  def auth(self) -> Either:
    either = AuthUserJsonRepository(self.__name, self.__password)
    if(type(either) == Right): 
      self.__resultAccount = either.result
      return -1
    return either.code  