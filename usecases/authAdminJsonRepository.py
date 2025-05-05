import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs


def AuthAdminJsonRepository(number) -> Either:
  admin = getEndpointJson(AppURLs.authAdmin)
  if(type(admin) == Left): return admin
  value = admin.get(str(number)) 
  if(value == None): return Left(ValueError, 1)
  return Right(value)
  


# testes 
# print(AuthUserJsonRepository("abc", "1567")) # should return login not found
# print()
# print(AuthUserJsonRepository("mateus", "1234567").message) # should return failure
# print()
# print(AuthUserJsonRepository("mateus", "12345678").message) # should return success
