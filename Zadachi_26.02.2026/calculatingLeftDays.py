import datetime
import time

def calcDays():
  today = datetime.date.today()
  endPeriod = datetime.date(2027, 2, 26)
  leftDays = (endPeriod - today).days
  print(f"Today's date: {today}")
  time.sleep(2)
  print(f"Days left until the end of the year: {leftDays}")

if __name__ == "__main__":
  calcDays()