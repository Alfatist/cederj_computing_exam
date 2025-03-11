import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from usecases.accessingAccountJsonRepository import addMoneyToBalanceAccountJsonRepository
from usecases.addToStatementJsonRepository import addToStatementJsonRepository

from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

  

def taxCurrentAccountsJsonRepository(nextTax = 20) -> Left | dict:
  '''discount tax from current Accounts'''

  try:
    
    datesToDiscountXtaxByAccount = getEndpointJson(AppURLs.datesToDiscountXtaxByAccount)

    dateNow = datetime.today()
    dateNextMonth = (dateNow + timedelta(days=30)).strftime('%d/%m/%Y')
    dateNowStr = dateNow.strftime('%d/%m/%Y')
    
    

    dictIndexesToDiscount = datesToDiscountXtaxByAccount.get(dateNowStr)

    if(dictIndexesToDiscount == None or dictIndexesToDiscount == {}): 
      if(dictIndexesToDiscount == {}): 
        datesToDiscountXtaxByAccount.pop(dateNowStr)
        writeEndpointJson(AppURLs.datesToDiscountXtaxByAccount, datesToDiscountXtaxByAccount)
      return Right("No current Account to discount tax")
    
    
    if(datesToDiscountXtaxByAccount.get(dateNextMonth) == None): datesToDiscountXtaxByAccount[dateNextMonth] = datesToDiscountXtaxByAccount["default"]
    dictToInterate = dictIndexesToDiscount
    for index in dictToInterate: 
      
      valueToTax = dictIndexesToDiscount[index]

      dictIndexesToDiscount.pop(index)
      if(dictIndexesToDiscount == {}): datesToDiscountXtaxByAccount.pop(dateNowStr)

      datesToDiscountXtaxByAccount[dateNextMonth][index] = nextTax
      
      addMoneyToBalanceAccountJsonRepository(index, -nextTax, False, False)
      addToStatementJsonRepository(index, f"Desconto mensal fixo de {valueToTax}.")
      writeEndpointJson(AppURLs.datesToDiscountXtaxByAccount, datesToDiscountXtaxByAccount)
      


  except Exception as e:
    return Left(e)
