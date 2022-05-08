import re
import datetime
import requests
import sys
from bs4 import BeautifulSoup

today = datetime.date.today() # 오늘 날짜
yester = today - datetime.timedelta(days=1) # 어제 날짜
next = today + datetime.timedelta(days=1) # 내일 날짜

try: response  = requests.get("https://www.weather.go.kr/w/eqk-vol/search/korea.do?schOption=&startTm="+str(yester)+"endTm="+str(today)+"&dpType=a") # 기상청 지진조회
except requests.exceptions.Timeout as errd:
   print("Timeout Error:", errd)
   sys.exit(0)
except requests.exceptions.ConnectionError as errc:
   print("Error Connecting: ", errc)
   sys.exit(0)
except requests.exceptions.HTTPError as errb:
   print("Http Error:", errb)
   sys.exit(0)
except requests.exceptions.RequestException as erra:
   print("AnyException: ", erra)
   sys.exit(0)
   
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
            Lat = tds[-5].text # 위도
            long = tds[-4].text # 경도

# 미소지진 분류

if mag < str(2):
       type = "미소지진"
else:
       type = "지진"

# KAKAO TTS 대응 ( 숫자 변환 )

def switch(mmir):
       global mmi2
       mmi2 = { "Ⅰ" : "1", "Ⅱ" : "2", "Ⅲ" : "3", "Ⅳ" : "4", "Ⅴ" : "5", "Ⅵ" : "6", "Ⅶ" : "7", "Ⅷ" : "8", "Ⅸ" : "9", "Ⅹ" : "10"  }.get(mmir, "진도 불명")
       print (origin_time,"에", address + "에서 규모",mag,"깊이", depth, "최대진도", mmi2 + "의", type, "이 발생하였습니다.")

switch(mmi)

REST_API_KEY = "SECRET"

class KTTS:

   def __init__(self, text, API_KEY=REST_API_KEY):
      try: self.resp = requests.post(
         url="https://kakaoi-newtone-openapi.kakao.com/v1/synthesize",
         headers={
            "Content-Type": "application/xml",
            "Authorization": f"KakaoAK {API_KEY}"
         },
         data=f"<speak>{text}</speak>".encode('utf-8')
      )
      except requests.exceptions.Timeout as errd:
         print("Timeout Error: ", errd)
         sys.exit(0)
      except requests.exceptions.ConnectionError as errd:
         print("Error Connnecting: ", errc)
         sys.exit(0)
      except requests.exceptions.HTTPError as errb:
         print("HTTP Error: ", errb)
         sys.exit(0)
      except requests.exceptions.RequestException as erra:
         print("AnyException :", erra)
         sys.exit(0)


   def save(self, filename="output.mp3"):
      with open(filename, "wb") as file:
         file.write(self.resp.content)


if __name__ == '__main__':
   tts = KTTS(origin_time + "에" + address + "에서 규모" + mag + "에" + type + "이 발생하였습니다. 최대진도는" + mmi2 + "입니다.")
   tts.save("tts.mp3")
