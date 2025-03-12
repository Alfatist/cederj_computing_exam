import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.getEndpointJson import getEndpointJson
from core.either.left import Left
from common.helpers.writeEndpointJson import writeEndpointJson
from core.constants.appURLs import AppURLs
from usecases.addMoneyToSpecialCheckJsonrepository import addMoneyToSpecialCheckJsonrepository
from usecases.getValueToTaxFromSpecialCheckJsonRepository import getValueToTaxFromSpecialCheckJsonRepository
from core.either.either import Either
from core.either.right import Right


def paySpecialCheckJsonRepository(account:str) -> Either:
  '''Pay check special with balance. Also include in statement and yield if needed'''

  specialCheckToPay = getValueToTaxFromSpecialCheckJsonRepository(account)
  
  if(specialCheckToPay > 0):
    accounts = getEndpointJson(AppURLs.accounts)
    balance = accounts[account]["balance"]
  
    if(balance > specialCheckToPay): 
      accounts[account]["balance"] -= specialCheckToPay
      addMoneyToSpecialCheckJsonrepository(account, specialCheckToPay)  
    else:
      accounts[account]["balance"] -= specialCheckToPay
      addMoneyToSpecialCheckJsonrepository(account, balance)

    return writeEndpointJson(AppURLs.accounts, accounts)
  return Left(ValueError, 13)