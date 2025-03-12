from datetime import datetime
from core.either.left import Left
from usecases.getAvailableCheckJsonRepository import getAvailableCheckJsonRepository
from usecases.getValueToTaxFromSpecialCheckJsonRepository import getValueToTaxFromSpecialCheckJsonRepository
from usecases.getStatementOfAccountJsonRepository import getStatementOfAccountJsonRepository
from usecases.accessingAccountJsonRepository import addMoneyToBalanceAccountJsonRepository, changeHolderAddressJsonRepository, checkIfAccountExistJsonRepository, getAddressAccountJsonRepository, getBalanceAccountJsonRepository, transferMoneyAccountJsonRepository
from core.either.either import Either
from core.either.right import Right
from usecases.orderDeleteAccountJsonRepository import orderDeleteAccountJsonRepository
from usecases.paySpecialCheckJsonRepository import paySpecialCheckJsonRepository
from usecases.removeMoneyFromBalanceAccountJsonRepository import removeMoneyFromBalanceAccountJsonRepository


class AccessingAccountController(object):
  __holderName:str
  __accountId:str
  def __init__(self, name:str, accountId:str): self.__holderName, self.__accountId = name, accountId

  def getName(self): return self.__holderName
  def getAccountId(self): return self.__accountId

  def addMoney(self, number: float) -> Either:
    if(number < 0): return Left(ValueError, 8)
    return addMoneyToBalanceAccountJsonRepository(self.__accountId, number)
  
  def withdrawMoney(self, number: float) -> Either:
    if(number < 0): return Left(ValueError, 8)
    return removeMoneyFromBalanceAccountJsonRepository(self.__accountId, number)

  def getBalance(self) -> float: return getBalanceAccountJsonRepository(self.__accountId)
  def getAvailableCheck(self) -> Left | float: return getAvailableCheckJsonRepository(self.__accountId)
  def getValueToPaySpecialCheck(self) -> Left | float: return getValueToTaxFromSpecialCheckJsonRepository(self.__accountId)
  def getAddress(self) -> Either: return getAddressAccountJsonRepository(self.__accountId)
  
  def checkAccountExist(self, accountToCheck:str) -> bool: 
    if(not accountToCheck.isnumeric()): return False
    return checkIfAccountExistJsonRepository(accountToCheck)
  
  def transferMoneyToAccount(self, accountToTransfer:str, value: float) -> Either:
    if(0 < value < self.getBalance() and accountToTransfer.isnumeric()): return transferMoneyAccountJsonRepository(str(self.__accountId), str(accountToTransfer), value)
    return Left(ValueError, 12)
  
  def isDateInRange(self, date_str, start_date_str, end_date_str, date_format="%d/%m/%Y"):
    try:
        date = datetime.strptime(date_str, date_format)
        start_date = datetime.strptime(start_date_str, date_format)
        end_date = datetime.strptime(end_date_str, date_format)
        return start_date <= date <= end_date
    except ValueError:
        return False
    
  def getStatementOfAccount(self, dateEntry = "", dateEnding = "") -> str:
    statementResponse = getStatementOfAccountJsonRepository(self.__accountId)
    responseType = type(statementResponse)
    if(responseType == Right):
      jsonStatementAccount = statementResponse.result
      if (jsonStatementAccount == None or jsonStatementAccount == {}): return "Não há extrato para esta conta."
      fullStatementToString = ""
      dates = list(jsonStatementAccount.keys())
      if(dateEntry == "" and dateEnding == ""):
        for date in dates:
          fullStatementToString += f"{date}:\n\n"
          fullStatementToString += f"{"\n".join(jsonStatementAccount[date])}\n\n"
        return fullStatementToString
      try:
        datetime.strptime(dateEntry, "%d/%m/%Y")
        datetime.strptime(dateEnding, "%d/%m/%Y")  
      except:
        return "Desculpe, tente novamente com uma data válida."
      
      
      for date in dates:
        if(self.isDateInRange(date, dateEntry, dateEnding)):
          fullStatementToString += f"{date}:\n\n"
          fullStatementToString += f"{"\n".join(jsonStatementAccount[date])}\n\n"
      if(fullStatementToString == "" ): return "Não há extrato para a data especificada."
      return fullStatementToString
      
    return "Desculpe, tivemos um erro ao tentar pegar o extrato."
    
  def changeHolderAddress(self, newAddress) -> Either: return changeHolderAddressJsonRepository(self.__accountId, newAddress)

  def orderDeleteAccount(self): return orderDeleteAccountJsonRepository(self.__accountId, self.__holderName)

  def paySpecialCheck(self) -> Either:
    balance = self.getBalance() 
    if(balance <= 0): return Left(ValueError, 11)
    valueToPay = self.getValueToPaySpecialCheck()
    if(balance > valueToPay): balance = valueToPay
    return paySpecialCheckJsonRepository(self.__accountId)
