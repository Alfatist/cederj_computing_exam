from datetime import datetime, timedelta
import sys
import os

from usecases.addAccountToUserJsonRepository import addAccountToUserJsonRepository
from usecases.addMoneyToSpecialCheckJsonrepository import addMoneyToSpecialCheckJsonrepository

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

def createCurrentAccountJsonRepository(holderName, address, agency = "0001", taxMonthly = 20) -> Either:
  try:
    accounts = getEndpointJson(AppURLs.accounts)
    if(type(accounts) == Left): return accounts

    datesToDiscountXtaxByAccount = getEndpointJson(AppURLs.datesToDiscountXtaxByAccount)
    if(type(datesToDiscountXtaxByAccount) == Left): return accounts

    dateNow = datetime.today()
    dateNextMonth = (dateNow + timedelta(days=30)).strftime('%d/%m/%Y')

    
    accountID = accounts["nextId"]

    datesToDiscountXtaxByAccount[accountID] = datesToDiscountXtaxByAccount["default"].copy()
    datesToDiscountXtaxByAccount[accountID][dateNextMonth] = taxMonthly

    accounts["nextId"] = accountID + 1
    newJson = accounts["defaultCurrentAccountDict"].copy()
    newJson["holderName"] = holderName
    newJson["holderAddress"] = address
    newJson["agency"] = agency
    accountID = str(accountID)

    accounts[accountID] = newJson
    either = writeEndpointJson(AppURLs.accounts, accounts)
    if(type(either) == Right): 
      resultTax = writeEndpointJson(AppURLs.datesToDiscountXtaxByAccount, datesToDiscountXtaxByAccount)
      if(type(resultTax) == Right): 
        addMoneyToSpecialCheckJsonrepository(accountID, 0)
        addAccountToUserJsonRepository(holderName, accountID)
        return Right(str(accountID))
    return Left(ConnectionError, 5)
  except Exception as e:
    return Left(e)