import re
import datetime
import requests
from bs4 import BeautifulSoup

today = datetime.date.today()

response  = requests.get("https://www.weather.go.kr/w/eqk-vol/search/korea.do?schOption=&startTm=2022-01-01endTm="+str(today)+"&dpType=a")
soup = BeautifulSoup(response.content, 'html.parser')


first = soup.select("#excel_body > tbody > tr:nth-child(1)")

for tr in first: # #excel_body > tbody > tr:nth-child(1) 항목 검색
    tds = list(tr.find_all('td')) # td 리스트화 
    for td in tds: # td 검색
        if td.find('a'): # 기준점을 a herf 부분으로 잡음.
            number = tds[-10].text
            origin_time = tds[-9].text
            mag = tds[-8].text 
            depth = tds[-7].text + "km"
            mmi = tds[-6].text
            address = tds[-3].text

# KAKAO TTS 대응 ( 숫자 변환 )

mmi = mmi.replace('Ⅰ','1') # JMA 0
mmi = mmi.replace('Ⅱ','2') # JMA 0 ~ 1
mmi = mmi.replace('Ⅲ','3') # JMA 1 ~ 2
mmi = mmi.replace('Ⅳ','4') # JMA 2 ~ 3
mmi = mmi.replace('Ⅴ','5') # JMA 3 ~ 4
mmi = mmi.replace('Ⅵ','6') # JMA 4 ~ 5-
mmi = mmi.replace('Ⅶ','7') # JMA 5+ ~ 6-
mmi = mmi.replace('Ⅷ','8') # JMA 6- ~ 6+
mmi = mmi.replace('Ⅸ','9') # JMA 6+ ~ 7
mmi = mmi.replace('Ⅹ','10') # JMA 7

print (origin_time,"에", address + "에서 규모",mag,"깊이", depth + "최대진도", mmi + "의 지진이 발생하였습니다.")

REST_API_KEY = "SECRET"

class KTTS:

   def __init__(self, text, API_KEY=REST_API_KEY):
      self.resp = requests.post(
         url="https://kakaoi-newtone-openapi.kakao.com/v1/synthesize",
         headers={
            "Content-Type": "application/xml",
            "Authorization": f"KakaoAK {API_KEY}"
         },
         data=f"<speak>{text}</speak>".encode('utf-8')
      )

   def save(self, filename="output.mp3"):
      with open(filename, "wb") as file:
         file.write(self.resp.content)


if __name__ == '__main__':
   tts = KTTS(origin_time + "에" + address + "에서 규모" + mag + "의 지진이 발생하였습니다. 최대진도는" + mmi + "입니다.")
   tts.save("tts.mp3")
