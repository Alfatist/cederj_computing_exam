import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from usecases.removeMoneyFromBalanceAccountJsonRepository import removeMoneyFromBalanceAccountJsonRepository
from usecases.getValueToTaxFromSpecialCheckJsonRepository import getValueToTaxFromSpecialCheckJsonRepository
from usecases.addMoneyToSpecialCheckJsonrepository import addMoneyToSpecialCheckJsonrepository 
from usecases.addToStatementJsonRepository import addToStatementJsonRepository
from usecases.addToYieldRepository import addToYieldJsonRepository
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs 

def changeHolderAddressJsonRepository(account, newAddress) -> Either:
  try:
    newJson = getEndpointJson(AppURLs.accounts)
    if(newJson == Left): return newJson
    newJson[account]["holderAddress"] = newAddress
    return writeEndpointJson(AppURLs.accounts, newJson)
  except Exception as e:
    return Left(e)