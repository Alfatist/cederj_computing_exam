import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

def getAccountJsonRepository(idAccount) -> Left | dict:
  try: 
    accounts = getEndpointJson(AppURLs.accounts)
    account = accounts.get(idAccount)
    if(account == None): return Left(ValueError, 1)
    return accounts.get(idAccount)
  except: return Left(Exception)
