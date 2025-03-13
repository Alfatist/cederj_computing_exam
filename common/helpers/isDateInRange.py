from datetime import datetime


def isDateInRange(date_str, start_date_str, end_date_str, date_format="%d/%m/%Y") -> bool:
    try:
        date = datetime.strptime(date_str, date_format)
        start_date = datetime.strptime(start_date_str, date_format)
        end_date = datetime.strptime(end_date_str, date_format)
        return start_date <= date <= end_date
    except ValueError:
        return False