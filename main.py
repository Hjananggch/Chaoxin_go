from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import json
import re
from datetime import datetime, timedelta
from urllib.parse import quote
import time


class Chaoxing_go():
    def __init__(self,uname,pwd):
        self.username = uname
        self.pwd = pwd
        self.seat_id = None
        self.roomid = None
        self.requests = requests.Session()
        self.page_roomid_url = 'https://reserve.chaoxing.com/data/apps/seatengine/room/list?time=&cpage=1&pageSize=100&firstLevelName=&secondLevelName=&thirdLevelName=&day=2024-09-12&deptIdEnc=79b034b1ae3bfe23&seatId=709'
        self.headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/128.0.0.0",
        "cookie": 'SECKEY_ABVK=14GJ3YAWLhXJK38vror9/z2FCd/QrvvF8S3Q8BYoR9U%3D; BMAP_SECKEY=4qmG2vHArS4aoRZnqwW6g1dlZ7unNZYFdf4BOVkSGrzcjenFtvtt4h2vyq-rsqgNYWbdkzjOenF8PXNBihNsvF_XqvmR0kr3a72Kpd_5-YrCD3xoylWjKuRAnOPSkGUhS-BYvvl8SWZAMwq_oiyINg_Mqis152NObDrjJudq7CX3ptW830n8tZI0hOY1oTjrNp5GsuYfLYD4wSVymWj-isV-rlo4dLC6QL5VOlSNhU8; fid=531; lv=2; _uid=205040813; UID=205040813; vc=AF8A2507BA08BAAF82257A9E9D6EF734; vc2=AA7B0596F49EB7F3393626D3A01BA83D; xxtenc=3bde6af760645bf04f2126810be0f5e0; createSiteSource=num8; wfwfid=531; source=num2; workRoleBenchId=0; siteType=2; wfwEnc=9DDE540B66DD52DC9B7BA54DF0859ECC; uf=569b376a64ccf0319a3481631043483a83f791ee56509ec34b46b399d41c2f6a07b859a0bdc776347aa7934e67265253c49d67c0c30ca5047c5a963e85f11099b9062f300db9572fce71fc6e59483dd399b7a34fa98db50179a4cd0a24971602b8b560ea7b9d4b48; _d=1725974777305; vc3=CoNO5n7Yy%2BbNRC0PBgQ3FIXCtmYprevWI8kIT2%2BHA7QU6ntNA8V%2BoMCOPRBGBImYaEVvStW%2Fg6AiXbXT1PSu6t7SgC%2F3mmeAU89kvlGinGfaPGmjkfEo2NiI9cxQQ2hY9BOX1FsiS1iY%2F3kBT8lbsQHU13sGp%2BnVbGcVCipcLfg%3Da4660003807a61468222ba01b637d91a; cx_p_token=b5a6545f6f47bc713e0a74baf8d5f0bb; p_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyMDUwNDA4MTMiLCJsb2dpblRpbWUiOjE3MjU5NzQ3NzczMDcsImV4cCI6MTcyNjU3OTU3N30.27P8NUkMZMRHFn7HZtANU3_gMreD7BgkzQzvDaGKqV4; DSSTASH_LOG=C_38-UN_624-US_205040813-T_1725974777307; oa_uid=205040813; oa_name=%E8%AE%B8%E5%BF%A0%E5%AF%8C; route=e37b564281be6bf42f59a301ebbe05b5; JSESSIONID=36B4D3674FC1B416102D8F9F262FAEA4.reserve_web_127; oa_deptid=531; oa_enc=35eb44a23256b59219ca21fe5d5fa7bf'
    }

    def get_roomid(self):
        page_roomid_res = self.requests.get(url=self.page_roomid_url,headers=self.headers)
        data = json.loads(page_roomid_res.text)
        if data['success']:
            # 遍历每个房间的数据
            for room in data['data']['seatRoomList']:
                room_id = room['id']
                first_level_name = room['firstLevelName']
                second_level_name = room['secondLevelName']
                third_level_name = room['thirdLevelName']

                # 格式化输出
                output = f"{first_level_name}{second_level_name}{third_level_name}roomid为{room_id}"
                print(output)

    def get_room_lists(self):
        self.get_roomid()

        self.roomid = input("请输入房间id:")
        start_time = self.get_validated_time("请输入开始预约的时间（如08:00）: ")
        end_time = self.get_validated_time("请输入结束预约的时间（如22:30）: ", start_time)

        start_time_encoded = quote(start_time)
        end_time_encoded = quote(end_time)

        current_date = datetime.now()
        self.formatted_date = current_date.strftime('%Y-%m-%d')
        set_url = f'https://office.chaoxing.com/data/apps/seatengine/seatgrid/roomid?roomId={self.roomid}'
        # set_a_url = f'https://office.chaoxing.com/data/apps/seatengine/getusedseatnums?seatId=709&roomId={self.roomid}&startTime={start_time_encoded}&endTime={end_time_encoded}&day={self.formatted_date}'
        set_a_url = 'https://office.chaoxing.com/data/apps/seatengine/getusedseatnums?seatId=709&roomId=1011&startTime=19%3A00&endTime=22%3A00&day=2024-09-12'
        res = requests.get(set_url, headers=self.headers)
        data_json = json.loads(res.text)

        seat_datas = data_json['data']['seatDatas']
        all_seat_nums = [seat['seatNum'] for seat in seat_datas]
        print("所有座位号:", ', '.join(sorted(all_seat_nums)))

        resq = requests.get(set_a_url, headers=self.headers)
        data_json = json.loads(resq.text)
        with open('data.json', 'w') as f:
            f.write(resq.text)
        # reserved_seats = data_json['data']['seatReserves']
        # all_reserved_seat_nums = [seat['seatNum'] for seat in reserved_seats]
        reserved_seats = data_json['data']['seatReserves']
        all_reserved_seat_nums = [seat['seatNum'] for seat in reserved_seats]
        print("已被预约的座位号:", ', '.join(sorted(all_reserved_seat_nums)))

        all_seat_nums_set = set(all_seat_nums)
        all_reserved_seat_nums_set = set(all_reserved_seat_nums)
        available_seats = all_seat_nums_set - all_reserved_seat_nums_set
        if len(available_seats):
            print("当前时间段可预约座位号:", ', '.join(sorted(available_seats)))
        else:
            print("当前时间段没有可预约座位")
            self.roomid = None


    def go_(self):
        self.username = self.username
        self.pwd = self.pwd
        self.seat_id = input("请输入座位号:")

        if not self.roomid:
            self.roomid = input("请输入房间id:")

        start_time = self.get_validated_time("请输入开始预约的时间（如08:00）: ")
        end_time = self.get_validated_time("请输入结束预约的时间（如22:30）: ", start_time)

        start_time = self.adjust_time(start_time, type=1)
        end_time = self.adjust_time(end_time, type=0)


        options = Options()
        driver = webdriver.Chrome(options=options)
        driver.get(
            f"https://office.chaoxing.com/front/third/apps/seatengine/select?id={self.roomid}&day={self.formatted_date}&backLevel=2&seatId=709&fidEnc=79b034b1ae3bfe23")

        try:
            wait = WebDriverWait(driver, 10)  # 增加等待时间以确保页面加载
            # 登录部分
            wait.until(EC.presence_of_element_located((By.ID, "phone"))).send_keys(self.username)
            wait.until(EC.presence_of_element_located((By.ID, "pwd"))).send_keys(self.pwd)
            wait.until(EC.element_to_be_clickable((By.ID, "loginBtn"))).click()

            print("登录成功！")
            start_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{start_time}')]"))
            )
            # 点击元素
            start_element.click()

            end_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{end_time}')]"))
            )
            # 点击元素
            end_element.click()

            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '确认')]"))
            )
            # 点击确认按钮
            confirm_button.click()

            seat = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f"//div[@class='grid_cell grid_seat'][contains(text(), '{self.seat_id}')]"))
                    )
            # 点击元素
            seat.click()

            time.sleep(10)

        finally:
            # 关闭浏览器
            driver.quit()

    def validate_time(self,input_time):
        pattern = re.compile(r"^(0[8-9]|1[0-9]|2[0-2]):([03]0)$")
        if not pattern.match(input_time):
            return False, None  # 时间格式不正确

        try:
            time_obj = datetime.strptime(input_time, '%H:%M')
        except ValueError:
            return False, None  # 时间解析失败

        start_limit = datetime.strptime("08:00", '%H:%M')
        end_limit = datetime.strptime("22:30", '%H:%M')

        if start_limit <= time_obj <= end_limit:
            return True, time_obj
        else:
            return False, None

    def get_validated_time(self,prompt, start_time=None):
        while True:
            user_time = input(prompt)
            is_valid, time_obj = self.validate_time(user_time)
            if is_valid:
                if start_time is not None and time_obj <= datetime.strptime(start_time, '%H:%M'):
                    print("结束时间必须大于开始时间，请重新输入。")
                else:
                    return time_obj.strftime('%H:%M')
            else:
                print("请输入有效的时间（HH:MM，分钟部分必须为00或30，时间从08:00到22:30）。")

    def adjust_time(self,time_str, type):
        # 将字符串时间转换为datetime对象
        current_time = datetime.strptime(time_str, "%H:%M")

        # 根据type确定时间调整
        if type == 1:
            # 往后延迟半小时
            start_time = current_time
            end_time = current_time + timedelta(minutes=30)
        elif type == 0:
            # 往前推半小时
            start_time = current_time - timedelta(minutes=30)
            end_time = current_time

        # 格式化开始时间和结束时间，生成结果字符串
        result = f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"
        return result



s = Chaoxing_go(19984,"Xzf10")
s.get_room_lists()
# s.go_()
