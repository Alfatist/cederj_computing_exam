import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from usecases.addMoneyToBalanceAccountJsonRepository import addMoneyToBalanceAccountJsonRepository 
from usecases.addToStatementJsonRepository import addToStatementJsonRepository
from core.either.left import Left
from core.either.right import Right 

def transferMoneyAccountJsonRepository(accountTransfering, accountToTransfer, value):
  try:
    addMoneyToBalanceAccountJsonRepository(accountTransfering, -value, False)
    addMoneyToBalanceAccountJsonRepository(accountToTransfer, value, False)
    addToStatementJsonRepository(accountTransfering ,f"Transferência de {value} reais para a conta de id {accountToTransfer}")
    addToStatementJsonRepository(accountToTransfer ,f"Transferência de {value} reais vindo da conta de id {accountTransfering}")

    return Right("Transferência realizada com sucesso")
    
  except Exception as e:
    return Left(e)
