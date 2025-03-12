import sys
import os

from usecases.getValueToTaxFromSpecialCheckJsonRepository import getValueToTaxFromSpecialCheckJsonRepository
from usecases.removeMoneyFromSpecialCheckJsonrepository import removeMoneyFromSpecialCheckJsonrepository
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from usecases.addToStatementJsonRepository import addToStatementJsonRepository

from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

  

def addMoneyToSpecialCheckJsonrepository(account, value) -> Left | float:
  '''Add money to special check. Negative values will remove.'''
  if(value == 0): return Left(ValueError, 7)
  if(value < 0): return removeMoneyFromSpecialCheckJsonrepository(account, -value)
  try:
    specialChecks = getEndpointJson(AppURLs.specialCheck)
    indexDictToReceive = specialChecks.get(account)
    if(indexDictToReceive == None or indexDictToReceive == {}): specialChecks[account] = specialChecks["default"]
    
    addToStatementJsonRepository(account, f"Pago {value} reais do cheque especial.")
      
    specialChecks[account]["checkAvailable"] += value
    specialChecks[account]["valueToTax"] -= value
    if(getValueToTaxFromSpecialCheckJsonRepository(account) < 0): specialChecks[account]["valueToTax"] = 0

    writeEndpointJson(AppURLs.specialCheck, specialChecks)
    return 

  except Exception as e:
    return Left(e)
