# -*- coding: utf-8 -*-
# @Time  : 2024-7-4 21:46:28
# @Author: 郭军
# @Email:391350540@qq.com
# @File  : login.py
# @Software: PyCharm
# @PythonVersion: python 3.12
# @Version : V1.0
# @Project: webportal
# @Description: 登陆页面
# @Update: 2024-7-4 21:46:28
# @UpdateContent:  登陆页面
import time

from pages.base import BasePage
from common.config import API_BASE_URL, WebPortal_username, WebPortal_password
from selenium.webdriver.common.by import By
from common.helpers import filter_requestWillBeSent
from selenium.webdriver.common.action_chains import ActionChains

class LoginPage(BasePage):
    def __init__(self,user=WebPortal_username,password=WebPortal_password):
        # 编写定位器和页面属性
        super().__init__()
        self.name_input_locator = (By.NAME, "email")
        self.passwd_input_locator = (By.NAME, "password")
        self.submit_button_locator = (By.CLASS_NAME, "ant-btn")
        self.username = user
        self.userpasswd = password
        self.url = "/sign-in"

    # """封装元素操作"""
    # 输入用户名
    def open(self, url: str = ""):
        self.driver.get(API_BASE_URL + url)
    def name_imput(self):
        self.enter_text(self.name_input_locator, self.username)

    # 输入密码
    def passwd_imput(self):
        self.enter_text(self.passwd_input_locator, self.userpasswd)

    # 点击登陆
    def click_submit(self):
        self.click(self.submit_button_locator)

    def get_network(self,driver):
        interface = filter_requestWillBeSent(driver)
        return interface

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



    def quit(self):
        self.driver.quit()

if __name__ == '__main__':
    # base = BasePage('chrome')
    # base.open(url=LoginPage.url)
    login = LoginPage()
    login.open(url=login.url)
    login.name_imput()
    login.passwd_imput()
    login.click_submit()
    time.sleep(6)
    login.logout()
