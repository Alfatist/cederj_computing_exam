from datetime import datetime


def getMaxDateAsString(listDates):
  '''Recevbe uma lista de datas no formato dd/mm/yyyy e retorna a maior data no formato dd/mm/yyyy'''
  listDateTime = []

  for date in listDates:
    listDateTime.append(datetime.strptime(date, '%d/%m/%Y'))

  maxDate = listDateTime[0]
  for date in listDateTime:
    if(date > maxDate): maxDate = date
  return maxDate.strftime("%d/%m/%Y")