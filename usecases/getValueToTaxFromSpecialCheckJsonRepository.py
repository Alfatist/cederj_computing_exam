import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.either.left import Left
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

def getValueToTaxFromSpecialCheckJsonRepository(accountID) -> Left | float:
  try: 
    specialChecks = getEndpointJson(AppURLs.specialCheck)
    return float(specialChecks[accountID]["valueToTax"])
  except Exception as e: return Left(e)
