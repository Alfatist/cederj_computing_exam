from datetime import datetime, timedelta
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.helpers.getEndpointJson import getEndpointJson
from common.helpers.writeEndpointJson import writeEndpointJson
from common.helpers.getMaxDateAsString import getMaxDateAsString
from common.helpers.verifyIfExistsInList import verifyIfExistsInList
from core.constants.appURLs import AppURLs


def addToYieldJsonRepository(account, value):
  balanceSavingsMonthsxAccount = getEndpointJson(AppURLs.balanceSavingsMonthsxAccount)
  balanceSavingsById = getEndpointJson(AppURLs.balanceSavingsbyId)

  dateNow = datetime.today()
  dateNextMonth = (dateNow + timedelta(days=30)).strftime('%d/%m/%Y')
  if(value > 0):
    if(balanceSavingsMonthsxAccount.get(dateNextMonth) == None): balanceSavingsMonthsxAccount[dateNextMonth] = balanceSavingsMonthsxAccount["default"]
    if(balanceSavingsById.get(account) == None): balanceSavingsById[account] = balanceSavingsById["default"]

    if(not verifyIfExistsInList(balanceSavingsMonthsxAccount[dateNextMonth], account)): 
      balanceSavingsMonthsxAccount[dateNextMonth].append(account)
    
    if(balanceSavingsById[account].get(dateNextMonth) == None): balanceSavingsById[account][dateNextMonth] = 0
    balanceSavingsById[account][dateNextMonth] += value
    
  else:
    listDates = list(balanceSavingsById[account].keys())
    listDates.remove("yield")
    value = -value

    while(value != 0):
      maxDate = getMaxDateAsString(listDates)
      valueToReduce = balanceSavingsById[account][maxDate]
      if(valueToReduce > value):
        balanceSavingsById[account][maxDate] -= value
        value = 0
        
      else:
        value -= valueToReduce
        balanceSavingsById[account].pop(maxDate)
        balanceSavingsMonthsxAccount[maxDate].remove(account)
        listDates.remove(maxDate)
        
  writeEndpointJson(AppURLs.balanceSavingsbyId, balanceSavingsById)
  return writeEndpointJson(AppURLs.balanceSavingsMonthsxAccount, balanceSavingsMonthsxAccount)