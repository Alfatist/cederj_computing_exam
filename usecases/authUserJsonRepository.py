import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.verifyIfExistsInList import verifyIfExistsInList
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs


def AuthUserJsonRepository(name, password) -> Either:
  users = getEndpointJson(AppURLs.accounts)
  if(type(users) == Left): return users

  if(users.get(name) == None): return Left(ValueError, 1)

  

  if(users[name]["agency"] == password): 
    user = users[name]["holderName"]
    clients = getEndpointJson(AppURLs.clients)
    
    result = verifyIfExistsInList(clients.get(user), name)
    if(result): return Right(user)
  return Left(ValueError, 2)


# testes 
# print(AuthUserJsonRepository("abc", "1567")) # should return login not found
# print()
# print(AuthUserJsonRepository("mateus", "1234567").message) # should return failure
# print()
# print(AuthUserJsonRepository("mateus", "12345678").message) # should return success
