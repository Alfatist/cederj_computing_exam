import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.either.left import Left
from core.either.right import Right
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

def getAvailableAccountsJsonRepository(name) -> Left | list:
  try:
    accounts = getEndpointJson(AppURLs.clients)
    if(type(accounts) == Left): return accounts
    availableAccounts = accounts.get(name)

    if(availableAccounts == None or availableAccounts == []): return []
    return availableAccounts
  except Exception as e: return Left(e)