import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.either.left import Left
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

def getSolicitationStatusJsonRepository(idAccount) -> Left | str:
  try: 
    accounts = getEndpointJson(AppURLs.accounts)
    account = accounts.get(idAccount)
    return account.get("delete_solicitation")
  except: return Left(Exception)
