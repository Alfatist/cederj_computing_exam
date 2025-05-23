import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

def addAccountToUserJsonRepository(user, account) -> Either:
  user = str(user)
  try:
    users = getEndpointJson(AppURLs.clients)
    if(users.get(user) == None): users[user] = []
    users[user].append(account)
    return writeEndpointJson(AppURLs.clients, users)
  except:
    return Left(Exception)