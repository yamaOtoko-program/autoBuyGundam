import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
from logging import StreamHandler, Formatter, INFO, getLogger
import random
import os
import shutil
import datetime

class auto_order:
    def __init__(self, userdata_dir ,passwd,secure_code=000):
        self.passwd = passwd
        self.userdata_dir = userdata_dir 
        self.secure_code = secure_code
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--lang=ja-JP')
        options.add_argument('--incognito')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36') 
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service,
                                        options=options)
        
    def watch_start(self,url, interval = 60,file_name = 'test'):  

        while True:
            
            self.driver.get(url)
            res = self.driver.find_elements(By.CLASS_NAME, "buyBtn")
            if len(res) == 0:
                datetime_now = datetime.datetime.now()
                datetime_str = datetime_now.strftime('%Y/%m/%d %H:%M:%S')
                print("[" + datetime_str + "] " + "not found")
            else:
                page_width = self.driver.execute_script('return document.body.scrollWidth')
                page_height = self.driver.execute_script('return document.body.scrollHeight')
                self.driver.set_window_size(page_width, page_height)
                time.sleep(random.randint(self.wait_min,self.wait_max))
                res[0].click()
                self.order(file_name)
            time.sleep(interval)
    def order(self,file_name):
        file_loc = './' + file_name
        if os.path.isdir(file_loc):
            shutil.rmtree(file_loc)
        os.makedirs(file_loc)

        print("1")
        time.sleep(1)
        self.driver.save_screenshot(file_loc + '/1.png')
        self.driver.find_elements(By.CLASS_NAME, "btnRed")[0].click()   
        time.sleep(1)
        print("2")
        self.driver.find_elements(By.CLASS_NAME, "yBtnStack")[0].click()
        time.sleep(1)
        name = self.driver.find_element(By.ID,"memberId")
        password= self.driver.find_element(By.ID,"password")
        name.send_keys(self.userdata_dir)
        password.send_keys(self.passwd)
        self.driver.save_screenshot(file_loc + '/2.png')
        self.driver.find_elements(By.ID, "js_i_login0")[0].click()
        time.sleep(1)
        self.driver.save_screenshot(file_loc + '/3.png')
        self.driver.find_elements(By.ID, "sc_i_buy")[0].click()
        print("3")
        time.sleep(1)
        secure = self.driver.find_element(By.NAME,"creditCard.securityCode")
        secure.send_keys(self.secure_code)
        self.driver.save_screenshot(file_loc + '/4.png')
        self.driver.find_elements(By.CLASS_NAME, "buyButton")[0].click()
        print("4")
        self.driver.save_screenshot(file_loc + '/finish.png')
        time.sleep(10)
    def quit(self):
        self.driver.quit()

model = auto_order(userdata_dir = "username",
                   passwd = "password",
                   secure_code=000)
model.watch_start( url ="URL", 
                   interval = 30,
                   file_name=  "")
model.quit()