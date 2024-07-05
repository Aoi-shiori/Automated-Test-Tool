# common/helpers.py
import json
import logging
from datetime import time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
import time
from common.config import WEBDRIVER_PATH, API_BASE_URL
from common.logger import logger

def setup_webdriver():
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

        driver = webdriver.Chrome(options=options)

        logger.info("WebDriver initialized successfully")
        return driver
    except WebDriverException as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        raise e


class Get_Login_Driver():
    def __init__(self):
        self.driver = setup_webdriver()
        self.driver.get(API_BASE_URL + "/sign-in")
        self.driver.find_element(By.NAME, "email").send_keys("jun@vivalink.com.cn")
        self.driver.find_element(By.NAME, "password").send_keys("Jun@1234")
        self.driver.find_element(By.CLASS_NAME, 'ant-btn').click()
        time.sleep(2)
        self.driver.implicitly_wait(10)
        # driver.get(API_BASE_URL+"/user-management/pm-management")  # 打开用户管理页面

        # driver.switch_to.window(driver.window_handles[-1])      # 定位到最新打开窗口
        # driver.switch_to.window(driver.window_handles[-2])      # 定位到倒数第二个窗口
        # driver.switch_to.window(driver.window_handles[0])        # 定位到第一个窗口

        # performance_log = driver.get_log("performance")  # 获取性能日志
        # interfaces = filter_requestWillBeSent(driver,performance_log)  # 获取性能日志


    def get_driver(self):
        return self.driver

    def quit_driver(self):
        self.driver.quit()


def assert_equal(actual, expected, message=None):
    assert actual == expected, message or f"{actual} does not equal {expected}"


def assert_in(substring, string, message=None):
    assert substring in string, message or f"{substring} not found in {string}"

def assert_not_in(substring, string, message=None):
    assert substring not in string, message or f"{substring} found in {string}"

def assert_not_equal(actual, expected, message=None):
    assert actual != expected, message or f"{actual} equals {expected}"

def assert_is_instance(obj, cls, message=None):
    assert isinstance(obj, cls), message or f"{obj} is not an instance of {cls}"

def assert_is_not_instance(obj, cls, message=None):
    assert not isinstance(obj, cls), message or f"{obj} is an instance of {cls}"


# 查找页面元素信息并返回
def find_element(driver, by, value):
    try:
        element = driver.find_element(by, value)
        return element
    except Exception as e:
        logger.error(f"Failed to find element: {e}")
        return None


def filter_type(type):
    """
    过滤掉不需要的请求
    :param type: 请求类型
    :return:
    """
    if type == "XHR":
        return True
    return False


def filter_method(_type: str):
    """
    过滤掉不需要的请求
    :param method: 请求方法
    :return:
    """
    types = [
        "Network.requestWillBeSentExtraInfo", "Network.loadingFinished", "Network.loadingFailed"
    ]
    if _type not in types:
        return True
    return False


def get_interface(url: str):
    # 从url中获取接口名称
    interface = url.split("/")[-3:]
    interface = "/".join(interface)
    return interface


# def filter_requestWillBeSent(driver, performance_log):
def filter_requestWillBeSent(driver):
    """
    过滤出requestWillBeSent请求和responseReceived请求信息,并返回接口信息和请求信息
    :param driver: WebDriver
    :param performance_log: 性能日志
    :return: interfaces
    """
    performance_log=driver.get_log("performance")

    interfaces = []

    for entry in performance_log:

        entry = json.loads(entry["message"])["message"]  # 解析performance日志
        # 获取method
        method = entry.get("method")
        type = entry.get("params").get("type")

        if "Network." in method and type == "XHR" and filter_method(method):

            # entry = json.dumps(entry, indent=3)
            # print(json.dumps(entry,indent=3))  # 打印每个performance日志条目

            if "Network.requestWillBeSent" in method:
                # print(json.dumps(entry, indent=3))  # 打印每个performance日志条目
                request_id = entry.get("params").get("requestId")

                # 判断是否存在url属性
                if "params" in entry:
                    if "request" in entry.get("params"):
                        url = entry.get("params").get("request").get("url")
                        api = get_interface(url)
                    else:
                        api = ""

                try:

                    resp = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                    body = resp.get("body")
                    body = json.loads(body)
                    # print(222,body)

                    method = entry.get("params").get("request").get("method")
                    url = entry.get("params").get("request").get("url")
                    # print(333,method)

                    if method == "POST":
                        request = entry.get("params").get("request").get("postData")
                    else:
                        request = entry.get("params").get("request").get("url")
                    # print(444,request)

                    in1 = {"interface": api, "url": url, "method": method, "request": request, "response": body}

                    interfaces.append(in1)

                except Exception as e:
                    # print(e)
                    continue
                finally:
                    pass
    return interfaces
