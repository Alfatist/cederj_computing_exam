import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from usecases.addMoneyToBalanceAccountJsonRepository import addMoneyToBalanceAccountJsonRepository
from usecases.addToStatementJsonRepository import addToStatementJsonRepository

from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

  

def yieldSavingAccountsJsonRepository() -> Left | dict:
  '''yield every account programmed to yield today'''
  try:
    
    balanceSavingsMonthsxAccount = getEndpointJson(AppURLs.balanceSavingsMonthsxAccount)
    balanceSavingsById = getEndpointJson(AppURLs.balanceSavingsbyId)

    dateNow = datetime.today()
    dateNextMonth = (dateNow + timedelta(days=30)).strftime('%d/%m/%Y')
    dateNowStr = dateNow.strftime('%d/%m/%Y')
    
    

    indexListToReceive = balanceSavingsMonthsxAccount.get(dateNowStr)
    nextMonthToYield = balanceSavingsMonthsxAccount.get(dateNextMonth)

    if(indexListToReceive == None or indexListToReceive == []): 
      indexListToReceive = []
      return Right("No savings Account to receive yield")
    
    
    if(nextMonthToYield == None): balanceSavingsMonthsxAccount[dateNextMonth] = []

    try: indexListToReceive.remove("default")
    except: pass
    
    for index in indexListToReceive: 
      percentage = balanceSavingsById[index]["yield"]
      
      oldValue = balanceSavingsById[index][dateNowStr]
      valueToReceive = balanceSavingsById[index][dateNowStr] * percentage

      balanceSavingsById[index][dateNextMonth] = oldValue + valueToReceive
      balanceSavingsById[index].pop(dateNowStr)
      balanceSavingsMonthsxAccount[dateNowStr].remove(index)
      if(balanceSavingsMonthsxAccount[dateNowStr] == []): balanceSavingsMonthsxAccount.pop(dateNowStr)
      balanceSavingsMonthsxAccount[dateNextMonth].append(index)
      
      addMoneyToBalanceAccountJsonRepository(index, valueToReceive, False, False)
      addToStatementJsonRepository(index, f"Rendimento de {valueToReceive} sobre o valor {oldValue}")
      writeEndpointJson(AppURLs.balanceSavingsbyId, balanceSavingsById)
      writeEndpointJson(AppURLs.balanceSavingsMonthsxAccount, balanceSavingsMonthsxAccount)
      


  except Exception as e:
    return Left(e)
