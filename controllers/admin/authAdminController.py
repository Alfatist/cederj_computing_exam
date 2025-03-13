from core.either.either import Either
from usecases.authAdminJsonRepository import AuthAdminJsonRepository


class AuthAdminController(object):
  __name:str
  __password:str
  
  def getName(self) -> str: return self.__name
  def getpassword(self) -> str: return self.__password
  
  def setName(self, name:str) -> None: self.__name = name
  def setPassword(self, password:str) -> None: self.__password = password

  def __init__(self, name = None, password = None):
    self.__name, self.__password = name, password

  def auth(self) -> Either: return AuthAdminJsonRepository(self.__name, self.__password)
    