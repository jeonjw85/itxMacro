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

def itx():
    try:
        file_path = "./"
        with open(file_path+"data.json", encoding='utf-8') as f:
            data = json.load(f)
            

        dt = datetime.datetime.now()
        driver = webdriver.Chrome(options=options)

        url = "https://www.letskorail.com/ebizprd/prdMain.do"
        driver.get(url)
        driver.implicitly_wait(7)

        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        time.sleep(0.7)

        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.7)

        driver.find_element(By.XPATH, "//input[@id='txtGoStart']").clear()
        driver.find_element(By.XPATH, "//input[@id='txtGoStart']").send_keys("평내호평")
        time.sleep(0.7)

        driver.find_element(By.XPATH, "//input[@id='txtGoEnd']").clear()
        driver.find_element(By.XPATH, "//input[@id='txtGoEnd']").send_keys("용산")
        time.sleep(0.7)

        driver.find_element(By.XPATH, "//img[@alt='달력']").click()
        time.sleep(0.7)

        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0.7)
        if dt.strftime("%m") == "12": nxtmonth = "01"
        else:
            if dt.strftime("%m").find("0") == 0:
                nxtmonth = "0" + str(int(dt.strftime("%m")) + 1)
            elif dt.strftime("%m").find("0") == -1:
                nxtmonth = str(int(dt.strftime("%m")) + 1)
            else:
                print("ERROR - 날짜계산오류")
        driver.find_element(By.XPATH, "//span[@id='d2023%s%s']" % (nxtmonth, dt.strftime("%d"))).click()
        time.sleep(0.7)

        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.7)

        Select(driver.find_element(By.XPATH, '//select[@id="time"]')).select_by_value('07')
        time.sleep(0.7)

        driver.find_element(By.XPATH, "//img[@alt='승차권예매']").click()
        time.sleep(0.7)

        print("%s:%s:%s - 예매설정완료" % (dt.hour, dt.minute, dt.second))
        
        try:
            alert1 = driver.switch_to.alert
            alert1.accept()
            time.sleep(0.7)

            driver.switch_to.window(driver.window_handles[0])
            time.sleep(0.7)
        except Exception as err:
            print(err)


        try:
            driver.find_element(By.XPATH, "//img[@name='btnRsv1_0']").click()
            time.sleep(2)
        except Exception as error:
            print("[error] 매진됐거나 오류발생")

        driver.find_element(By.XPATH, "//input[@id='txtMember']").send_keys(data['korail']['id'])
        time.sleep(0.3)
        driver.find_element(By.XPATH, "//input[@id='txtPwd']").send_keys(data['korail']['pw'])
        time.sleep(0.7)

        print("%s:%s:%s - 로그인성공" % (dt.hour, dt.minute, dt.second))

        driver.find_element(By.XPATH, "//img[@alt='확인']").click()
        time.sleep(0.7)

        alert4 = driver.switch_to.alert
        alert4.accept()
        time.sleep(0.7)

        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.7)
        # driver.quit()

    except Exception as error:
        print(error)
    else:
        print("%s:%s:%s - 예매성공!\n예약일자:2023%s%s\n예약시간:%s" % (dt.hour, dt.minute, dt.second, nxtmonth, dt.strftime("%d"), "07"))

    try:
        alert2 = driver.switch_to.alert
        alert2.accept()
        time.sleep(0.7)

        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.7)

        driver.find_element(By.XPATH, "//a[@title='결제하기']").click()
        time.sleep(0.7)

        driver.find_element(By.XPATH, "//input[@id='chk_smpl_sb']").click()
        time.sleep(0.7)

        driver.find_element(By.XPATH, "//a[@id='fnIssuing']").click()
        time.sleep(0.7)

        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0.7)
        
        driver.find_element(By.XPATH, "//p[@class='bank_bt_pay']").click()
        time.sleep(0.7)

        driver.find_element(By.XPATH, "//input[@name='inputPwd1']").send_keys(data['autopay']['1'])
        time.sleep(0.3)
        driver.find_element(By.XPATH, "//input[@name='inputPwd2']").send_keys(data['autopay']['2'])
        time.sleep(0.3)
        driver.find_element(By.XPATH, "//input[@name='inputPwd3']").send_keys(data['autopay']['3'])
        time.sleep(0.3)
        driver.find_element(By.XPATH, "//input[@name='inputPwd4']").send_keys(data['autopay']['4'])
        time.sleep(0.3)
        driver.find_element(By.XPATH, "//input[@name='inputPwd5']").send_keys(data['autopay']['5'])
        time.sleep(0.3)
        driver.find_element(By.XPATH, "//input[@name='inputPwd6']").send_keys(data['autopay']['6'])
        time.sleep(0.3)
        print("비밀번호 입력완료")
        driver.find_element(By.XPATH, "//p[@class='sp_bottom_bn']").click()
        time.sleep(0.3)
        
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.7)

        driver.switch_to.frame("mainframeSaleInfo")
        time.sleep(0.7)

        driver.find_element(By.XPATH, "//a[@id='btn_next2']").click()
        time.sleep(0.3)

        alert3 = driver.switch_to.alert
        alert3.accept()
        time.sleep(0.7)
        driver.switch_to.parent_frame()
        time.sleep(0.3)
        driver.switch_to.window(driver.window_handles[0])
    except Exception as error:
        print(error)
    else:
        print("%s:%s:%s - 결제성공!\n예약일자:2023%s%s\n예약시간:%s" % (dt.hour, dt.minute, dt.second, nxtmonth, dt.strftime("%d"), "07"))
        driver.quit()
if __name__ == "__main__":
    AlertMessage = input("정기자동예매가 아닌 단독파일을 실행했습니다.\n정기자동예매를 원할시 auto.py를 실행해주세요.\n엔터 입력시 자동예매를 시작합니다 : ")
    if AlertMessage == "":
        itx()
    else:
        print("프로그램을 종료합니다")
