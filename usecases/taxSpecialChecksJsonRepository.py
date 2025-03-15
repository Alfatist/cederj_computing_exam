from datetime import datetime, timedelta
import sys
import os

from usecases.addToStatementJsonRepository import addToStatementJsonRepository

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.getEndpointJson import getEndpointJson
from core.either.left import Left
from common.helpers.writeEndpointJson import writeEndpointJson
from core.constants.appURLs import AppURLs
from usecases.addMoneyToSpecialCheckJsonrepository import addMoneyToSpecialCheckJsonrepository
from usecases.getValueToTaxFromSpecialCheckJsonRepository import getValueToTaxFromSpecialCheckJsonRepository
from core.either.either import Either
from core.either.right import Right


def taxSpecialChecksJsonRepository() -> Either:
  '''Tax any account need to task.'''
  try:
  
    specialChecks = getEndpointJson(AppURLs.specialCheck)
    specialChecksKeys = list(specialChecks.keys())
    specialChecksKeys.remove("default")
    dateNow = datetime.today()
    dateNextMonth = (dateNow + timedelta(days=30)).strftime('%d/%m/%Y')
    dateNow = dateNow.strftime('%d/%m/%Y')

    for key in specialChecksKeys:
      keyDict = specialChecks[key]
      if(keyDict["dateToTax"] == dateNow): 
        valueToDiscount = 1 + specialChecks[key]["tax"]
        specialChecks[key]["valueToTax"] *= valueToDiscount
        specialChecks[key]["dateToTax"] = dateNextMonth
        addToStatementJsonRepository(key, f"{valueToDiscount} acrescido no débito do cheque especial.")

    
    return writeEndpointJson(AppURLs.specialCheck, specialChecks)
  except Exception as e:
    return Left(e, 13)