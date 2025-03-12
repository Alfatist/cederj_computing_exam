import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from usecases.addToStatementJsonRepository import addToStatementJsonRepository

from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

  

def removeMoneyFromSpecialCheckJsonrepository(account, value) -> Left | dict:
  '''Remove money from special check. Value can be negative.'''
  if(value == 0): return Left(ValueError, 7)
  if(value<0): value = -value

  try:
    specialChecks = getEndpointJson(AppURLs.specialCheck)
    indexDictToReceive = specialChecks.get(account)
    monthToTax = indexDictToReceive.get("dateToTax")

    if(indexDictToReceive == None or indexDictToReceive == {}): specialChecks[account] = specialChecks["default"]
    
    dateNow = datetime.today()
    dateNextMonth = (dateNow + timedelta(days=30)).strftime('%d/%m/%Y')
    if(monthToTax == None or monthToTax == ""): specialChecks[account]["dateToTax"] = dateNextMonth
    specialChecks[account]["checkAvailable"] -= value
    if(specialChecks[account]["checkAvailable"] < 0): return Left(ValueError, 8)
    specialChecks[account]["valueToTax"] += value
    
    addToStatementJsonRepository(account, f"Consumido {value} reais do cheque especial.")
    writeEndpointJson(AppURLs.specialCheck, specialChecks)

  except Exception as e:
    return Left(e)
