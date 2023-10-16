import app, requests, time, schedule
from bs4 import BeautifulSoup
from datetime import datetime
now = datetime.now()

def auto():
    url = "https://dotwotnm.jjw.workers.dev"
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        result = BeautifulSoup(html, "html.parser")
        if str(result) == "x":
            print("토,일에는 예매하지않음")
        else:
            print("자동실행 시작 - ")
            app.itx()
    else:
        print("ERROR - 접속실패")
# auto()
schedule.every().day.at("07:00").do(auto)
schedule.every().day.at("07:01").do(auto)
schedule.every().day.at("07:02").do(auto)

while True:
    schedule.run_pending()
    time.sleep(1)