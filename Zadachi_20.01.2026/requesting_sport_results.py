import requests
import re
from bs4 import BeautifulSoup
url = "https://gong.bg/livescore/efbet-liga/klasirane"

r = requests.get(url)  # Прави HTTP GET заявка и сваля посочената страница
print("Status code:", r.status_code)  # Принтира статус кода на отговора (200 е успешен отговор)
bs = BeautifulSoup(r.text, features="html.parser")  # r.text държи суровите данни или в този случай html
divs = bs.find_all("div", {"class": "team"})  # намери всички div елементи, който имат сложен class team
i = 1
for div in divs:  
    text = re.sub(r'^\s+|\s+$', '', div.text)  # Regex премахващ спейсовете преди/след
    if text != "Отбор":  # Пропускаме реда с Отбор
        print(f"{i} {text}")  # принтираме и увеличаваме брояча
        i += 1
