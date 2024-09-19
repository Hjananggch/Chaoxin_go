from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
from multiprocessing import Process
import datetime

options = Options()

def start_go(num):
    # 初始化 WebDriver
    driver = webdriver.Chrome(options=options)

    target_time = datetime.time(18, 00, 00)
    while True:
        current_time = datetime.datetime.now().time()
        if current_time > target_time:
            url = 'https://office.chaoxing.com/front/third/apps/seat/select?deptIdEnc=6eea2c5fa8b19583&id=11107&day=2024-09-18&backLevel=2&fidEnc=6eea2c5fa8b19583' #座位url
            driver.get(url)

            try:
                wait = WebDriverWait(driver, 10)  # 增加等待时间以确保页面加载
                # 登录部分
                wait.until(EC.presence_of_element_located((By.ID, "phone"))).send_keys("111")
                wait.until(EC.presence_of_element_located((By.ID, "pwd"))).send_keys("111")
                wait.until(EC.element_to_be_clickable((By.ID, "loginBtn"))).click()
                # 循环尝试预约座位直到成功
                success = False
                while not success:
                    try:
                        start_element = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), '10:00-10:30')]")) #自选时间段
                        )
                        # 点击元素
                        start_element.click()

                        end_element = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), '21:30-22:00')]")) #自选时间段
                        )
                        # 点击元素
                        end_element.click()

                        confirm_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '确认')]"))
                        )
                        # 点击确认按钮
                        confirm_button.click()

                        seat = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, f"//p[@class='order_num' and contains(text(), '{num}')]"))  ###需要调整class
                        )
                        # Click the seat
                        seat.click()

                        submit_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//p[@class='order_submit' and contains(text(), '提交')]"))  ###需要调整class
                        )
                        # 点击提交按钮
                        submit_button.click()

                        time.sleep(0.05)
                        success = True
                        print('预约成功！')

                    except TimeoutException:
                        print("重试中...")
                        driver.refresh()

            except WebDriverException as e:
                print(f"发生错误：{e}")


        # 程序休眠一秒，避免过度占用 CPU
        print(f"当前时间：{current_time}")
        time.sleep(1)


if __name__ == '__main__':
    p1 = Process(target=start_go, args=('006',)) # 座位号
    p2 = Process(target=start_go, args=('007',))
    p3 = Process(target=start_go, args=('008',))

    p1.start()
    p2.start()
    p3.start()


    p1.join()
    p2.join()
    p3.join()
























