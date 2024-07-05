# -*- coding: utf-8 -*-
# @Time  : 2024-7-4 21:46:28
# @Author: 郭军
# @Email:391350540@qq.com
# @File  : rpm.py
# @Software: PyCharm
# @PythonVersion: python 3.12
# @Version : V1.0
# @Project: webportal
# @Description: rmp页面
# @Update: 2024-7-4 21:46:28
# @UpdateContent:  rmp页面

import time
from pages.base import BasePage
from common.config import API_BASE_URL
from selenium.webdriver.common.by import By
from common.helpers import filter_requestWillBeSent
from selenium.webdriver.common.action_chains import ActionChains
from common.logger import logger
from common.config import WebPortal_username,WebPortal_password

class RpmPage(BasePage):
    def __init__(self,user=WebPortal_username,password=WebPortal_password):
        super().__init__()
        # 编写定位器和页面属性
        self.username = user
        self.userpasswd = password
        self.driver = self.get_login_driver()
        self.url = "/rpm/rt"
        self.rpm_last_upload_time_locator=(By.CLASS_NAME,"ecg-last-upload")
        self.rpm_locator = (By.CLASS_NAME, 'yahuikeji-dashboard-rpm-chart')
        self.last_upload_time_locator = (By.CLASS_NAME, 'ecg-last-upload')

    def open(self, url: str = ""):
        self.driver.get(API_BASE_URL + url)

    def get_network(self,driver):
        interface = filter_requestWillBeSent(driver)
        return interface

    def get_title(self):
        return self.driver.title

    def get_rpm_subjectID(self):
        subjectID = self.find_element(self.rpm_locator).find_element(By.TAG_NAME, 'span')
        return subjectID.text

    def get_rpm_subjectIDs(self):
        subjectIDs = self.find_elements(self.rpm_locator)
        return [subjectID.find_element(By.TAG_NAME, 'span').text for subjectID in subjectIDs]

    def get_rpm_user_last_upload_time(self,SubjectID):
        subjectIDs = self.find_elements(self.rpm_locator)
        idlist=[subjectID.find_element(By.TAG_NAME, 'span') for subjectID in subjectIDs]

        for id in idlist:
            if id.text == SubjectID:
                print(id.text)
                exist = self.wait_for_element(self.last_upload_time_locator)
                print(333,exist)
                if exist:
                    try:
                        time=id.find_element(By.XPATH, '../../../..').find_element(By.CLASS_NAME, 'ecg-last-upload').text
                        print(444,time)
                        return time
                    except:
                            return "No data"



    def logout(self):
        # 等待登录成功提示框消失
        time.sleep(5)
        # 定位悬停菜单的触发元素（例如，一个按钮或链接）
        hover_element = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/header/div/div[3]/div/div/div')

        # 首先，我们需要将ActionChains对象初始化
        action = ActionChains(self.driver)

        # 然后，使用move_to_element()来悬停
        action.move_to_element(hover_element).perform()

        # 为了让菜单完全打开，我们等待一下
        time.sleep(2)

        # 定位悬停菜单中你想点击的元素
        menu_item_to_click = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/ul/li[4]/span/div")

        # 现在，悬停菜单已经打开，我们可以点击其中的元素
        action.click(menu_item_to_click).perform()

if __name__ == '__main__':
    rpm = RpmPage()
    rpm.open(rpm.url)
    time.sleep(5)
    print(rpm.get_rpm_subjectID())
    print(rpm.get_rpm_subjectIDs())
    print(rpm.get_rpm_user_last_upload_time('999-777'))