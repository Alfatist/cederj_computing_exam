import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

def GetAvailableAccountsJsonRepository(name) -> Either:
  try:
    availableAccounts = getEndpointJson(AppURLs.clients).get(name)

    if(availableAccounts == None or availableAccounts == []): return Right("Success but doesn't exist", [])
    return Right(availableAccounts)
  except: return Left("Error while trying to get accounts")


def getAccountByIdJsonRepository(idAccount: any):
  idAccount = str(idAccount)
  account = getEndpointJson(AppURLs.accounts).get(idAccount)
  typeAccount = account.get("type")
  return f"{typeAccount} ({idAccount})"
