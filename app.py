from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select
import time, datetime
import json
options = webdriver.ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("--headless")
options.add_argument("no-sandbox")
options.add_argument('--mute-audio')

try:
    file_path = "./"
    with open(file_path+"data.json", encoding='utf-8') as f:
        data = json.load(f)
        

    dt = datetime.datetime.now()
    driver = webdriver.Chrome(options=options)

    url = "https://www.letskorail.com/ebizprd/prdMain.do"
    driver.get(url)
    time.sleep(0.7)

    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    time.sleep(0.7)

    driver.switch_to.window(driver.window_handles[0])
    time.sleep(0.7)

    xpath1 = "//input[@id='txtGoStart']"
    driver.find_element(By.XPATH, xpath1).clear()
    driver.find_element(By.XPATH, xpath1).send_keys("평내호평")
    time.sleep(0.7)

    xpath2 = "//input[@id='txtGoEnd']"
    driver.find_element(By.XPATH, xpath2).clear()
    driver.find_element(By.XPATH, xpath2).send_keys("용산")
    time.sleep(0.7)

    xpath3 = "//img[@alt='달력']"
    driver.find_element(By.XPATH, xpath3).click()
    time.sleep(0.7)

    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.7)

    if dt.strftime("%m") == "12": nxtmonth = "01"
    else: nxtmonth = dt.strftime("%m")+1
    xpath4 = "//span[@id='d2023%s%s']"
    driver.find_element(By.XPATH, xpath4 % (nxtmonth, dt.strftime("%d"))).click()
    time.sleep(0.7)

    driver.switch_to.window(driver.window_handles[0])
    time.sleep(0.7)

    Select(driver.find_element(By.XPATH, '//select[@id="time"]')).select_by_value('11')
    time.sleep(0.7)

    xpath5 = "//img[@alt='승차권예매']"
    driver.find_element(By.XPATH, xpath5).click()
    time.sleep(0.7)

    print("%s:%s:%s - 예매설정완료" % (dt.hour, dt.minute, dt.second))

    driver.switch_to.alert
    Alert(driver).accept()
    time.sleep(0.7)

    driver.switch_to.window(driver.window_handles[0])
    time.sleep(0.7)

    try:
        xpath7 = "//img[@name='btnRsv1_0']"
        driver.find_element(By.XPATH, xpath7).click()
        time.sleep(5)
    except Exception as error:
        print("[error] 매진됐거나 오류발생")

    #data['korail']['id']

    xpath8 = "//input[@id='txtMember']"
    xpath9 = "//input[@id='txtPwd']"
    driver.find_element(By.XPATH, xpath8).send_keys(data['korail']['id'])
    time.sleep(0.2)
    driver.find_element(By.XPATH, xpath9).send_keys(data['korail']['pw'])
    time.sleep(0.7)

    print("%s:%s:%s - 로그인성공" % (dt.hour, dt.minute, dt.second))

    xpath10 = "//img[@alt='확인']"
    driver.find_element(By.XPATH, xpath10).click()
    time.sleep(1)

    driver.switch_to.alert
    Alert(driver).accept()
    time.sleep(1)

    driver.quit()

except Exception as error:
    print(error)
else:
    print("%s:%s:%s - 예매성공!\n예약일자:2023%s%s\n예약시간:%s" % (dt.hour, dt.minute, dt.second, nxtmonth, dt.strftime("%d"), "11"))