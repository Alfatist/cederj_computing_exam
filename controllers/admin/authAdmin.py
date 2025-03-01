from core.either.either import Either
from core.either.left import Left
from core.either.right import Right
from updates.authAdminJsonRepository import AuthAdminJsonRepository


class AuthAdminController(object):
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

  def auth(self) -> Either:
    either = AuthAdminJsonRepository(self.__name, self.__password)
    if(type(either) == Right): return Right(-1)
    return Left(either.code, either.code)