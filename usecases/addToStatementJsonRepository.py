import sys
import os
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.helpers.writeEndpointJson import writeEndpointJson
from core.either.left import Left
from core.either.right import Right
from core.either.either import Either
from common.helpers.getEndpointJson import getEndpointJson
from core.constants.appURLs import AppURLs

def addToStatementJsonRepository(account, text) -> Either:
  dateNow = datetime.datetime.today().strftime('%d/%m/%Y')
  statements = getEndpointJson(AppURLs.statements)
  if(statements.get(account) == None ): statements[account] = {}
  if(statements[account].get(dateNow) == None):  statements[account][dateNow] = []    
  statements[account][dateNow].append(text)
  return writeEndpointJson(AppURLs.statements, statements)