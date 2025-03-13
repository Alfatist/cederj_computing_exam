import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.either.left import Left
from core.either.right import Right
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

def getAccountByIdJsonRepository(idAccount: any) -> Left | str:
  try:
    accounts = getEndpointJson(AppURLs.accounts)
    if(type(accounts) == Left): return accounts
    idAccount = str(idAccount)
    
    account = accounts.get(idAccount)
    typeAccount = account.get("type")
    return f"{typeAccount} ({idAccount})"
  except Exception as e: return Left(e)