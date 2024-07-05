# pages/base_page.py
import json
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from common.config import WEBDRIVER_PATH, API_BASE_URL as BASE_URL
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from common.logger import logger
from common.config import WebPortal_username,WebPortal_password

class BasePage:
    """
    初始化driver
    :param browser:浏览器名称
    """

    def __init__(self, browser="chrome"):
        if browser == "chrome":
            try:
                options = Options()
                # options.add_argument('--disable-offline-load-stale-cache')
                # options.add_argument('--disable-application-cache')  # 禁用应用缓存
                # options.add_argument('--no-sandbox')  # 禁用沙箱模式
                # options.add_argument('--disable-gpu')  # 禁用GPU硬件加速
                # options.add_argument('--disable-cache')  # 禁用缓存
                # options.add_argument('--disk-cache-size=0')  # 设置磁盘缓存大小为0
                # options.add_argument('incognito')  # 隐身模式
                # options.add_argument("--headless")  # 无头模式
                # driver = webdriver.Chrome(executable_path = WEBDRIVER_PATH, options=options)
                # options.add_argument("--remote-debugging-port=9222")
                # options.add_experimental_option('w3c', False)
                options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
                self.driver = webdriver.Chrome(options=options)
                logger.info("WebDriver initialized successfully")
            except WebDriverException as e:
                logger.error(f"Failed to initialize WebDriver: {e}")
                raise e
        elif browser == "firefox":
            self.driver = webdriver.Firefox()
        elif browser == "ie":
            self.driver = webdriver.Ie()
        else:
            self.driver = None
            print("请输入正确的浏览器,例如:chrome,firefox,ie")

        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 20)
        self.name_input_locator = (By.NAME, "email")
        self.passwd_input_locator = (By.NAME, "password")
        self.submit_button_locator = (By.CLASS_NAME, "ant-btn")
        self.userpasswd = WebPortal_password
        self.username = WebPortal_username

    def open(self, url: str = ""):
        self.driver.get(BASE_URL + url)
        time.sleep(3)

    def find_element(self, locator: tuple):
        return self.driver.find_element(*locator)

    def find_elements(self, locator: tuple):
        return self.driver.find_elements(*locator)

    def wait_for_element(self, locator: tuple):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_element_not_exist(self, locator: tuple):
        return self.wait.until_not(EC.invisibility_of_element_located(locator))

    def click(self, locator: tuple):
        self.find_element(locator).click()
        time.sleep(3)

    def enter_text(self, locator: tuple, text: str):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_title(self):
        return self.driver.title

    def get_login_driver(self):
        self.open(url="/sign-in")
        self.enter_text(self.name_input_locator, self.username)
        self.enter_text(self.passwd_input_locator, self.userpasswd)
        self.click(self.submit_button_locator)
        return self.driver

    def quit(self):
        self.driver.quit()




if __name__ == '__main__':
    base = BasePage('chrome')
    base.open(url="/sign-in")
    base.enter_text(('name', 'email'), '111')