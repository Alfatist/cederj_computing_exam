import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs


def createUserJsonRepository(name, password) -> Either:
  try:
    if(len(password) < 8 ): return Left(ValueError, 4)

    users = getEndpointJson(AppURLs.authClients)
    if(type(users) == Left): return users

    if(users.get(name) != None): return Left(ValueError, 3)
    users[name] = {"password": password}
    return writeEndpointJson(AppURLs.authClients, users)
  except Exception as e: return Left(e)