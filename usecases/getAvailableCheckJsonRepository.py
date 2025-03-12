import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

def getAvailableCheckJsonRepository(accountID) -> Left | float:
  try: 
    specialChecks = getEndpointJson(AppURLs.specialCheck)
    return float(specialChecks[accountID]["checkAvailable"])
  except Exception as e: return Left(e)
