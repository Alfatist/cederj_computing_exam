import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs


def CreateUserJsonRepository(name, password) -> Either:
  if(len(password) < 8 ): return Left("", 4)
  users = getEndpointJson(AppURLs.authClients)

  if(users.get(name) != None): return Left("", 3)
  users[name] = {"password": password}
  return writeEndpointJson(AppURLs.authClients, users)
  
  
  


# testes 
# print(CreateUserJsonRepository("mateus", "123456789").message) # should return an account exist
# print(CreateUserJsonRepository("Mateus", "123456789").message) # should rewrite the json
# print(CreateUserJsonRepository("mateus", "123456789").message) # should rewrite the json