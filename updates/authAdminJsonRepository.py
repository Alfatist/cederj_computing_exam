import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs


def AuthAdminJsonRepository(name, password) -> Either:
  admin = getEndpointJson(AppURLs.authAdmin)

  if(admin.get(name) == None): return Left("", 1)

  if(admin[name]["password"] == password): return Right("deu certo!!")
  return Left("deu errado.", 2)


# testes 
# print(AuthUserJsonRepository("abc", "1567")) # should return login not found
# print()
# print(AuthUserJsonRepository("mateus", "1234567").message) # should return failure
# print()
# print(AuthUserJsonRepository("mateus", "12345678").message) # should return success
