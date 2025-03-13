import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from usecases.removeMoneyFromBalanceAccountJsonRepository import removeMoneyFromBalanceAccountJsonRepository
from usecases.addToStatementJsonRepository import addToStatementJsonRepository
from usecases.addToYieldRepository import addToYieldJsonRepository
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs 

def getBalanceAccountJsonRepository(account) -> Left | float:
  try: return float(getEndpointJson(AppURLs.accounts)[account]["balance"])
  except Exception as e: return Left(e)