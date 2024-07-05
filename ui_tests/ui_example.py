# ui_tests/
import json
import time
import allure

from common.createReport import create_report
from common.logger import logger
import pytest
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait

from common.helpers import setup_webdriver, assert_in, assert_equal, filter_requestWillBeSent, find_element, \
    Get_Login_Driver
from common.config import API_BASE_URL, Rpm_Page, User_Management_Page, Login_Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# 设置 ChromeDriver
login_driver = Get_Login_Driver().get_driver()

@pytest.mark.ui
@pytest.mark.env(test="dev")
@allure.title("UI Test Example")
def test_ui_example(driver=login_driver):
    try:
        interfaces = filter_requestWillBeSent(driver)  # 获取性能日志


        # print(111,interfaces)

        email_path ='//*[@id="root"]/div/div/div/div/div/div/main/div/div/div[2]/div[2]/div/div/div/div/div/div/div/table/tbody/tr/td[4]'
        email= find_element(driver,By.XPATH,email_path).text
        for i in interfaces:
            if i.get("interface") == "api/v1/currentUserInfo":
                assert_in(i.get("response").get("email"),email,"email is not equal\n")
                assert_equal(i.get("response").get("email"),email,"email is not equal\n")

        # assert_in("Program", driver.title, "Title does not contain 'Program'")

        # assert "百度" in driver.title
    finally:
        pass

@pytest.mark.ui
@allure.title("UI Test Login Check")
def test_ui_logincheck(driver=login_driver):
    driver.get(API_BASE_URL + User_Management_Page) # 打开用户管理页面
    time.sleep(2)
    email_path = '//*[@id="root"]/div/div/div/div/div/div/main/div/div/div[2]/div[2]/div/div/div/div/div/div/div/table/tbody/tr/td[4]'
    email=find_element(driver,By.XPATH,email_path).text
    interfaces = filter_requestWillBeSent(driver)
    try:
        for i in interfaces:
            if "backend/currentUserInfo/" in i.get("interface"):
                logger.info(f"接口获取到的登陆Email: {i.get("response").get("email")}")
                assert_in(i.get("response").get("email"), email, "email is not equal\n")
                assert_equal(i.get("response").get("email"), email, "email is not equal\n")
    finally:
        pass

@pytest.mark.ui
@allure.title("UI Test RPM")
def test_ui_RPM(driver=login_driver):
    driver.get(API_BASE_URL + Rpm_Page)  # 打开用户管理页面
    element_name="ecg-last-upload"
    try:
        Last_upload = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CLASS_NAME,element_name))).text
        logger.info(f"Last upload is {Last_upload}")

        assert_in("Last upload",Last_upload,"Last Upload is not equal\n")

    finally:
        driver.quit()


@allure.story("UI Test Login")
@pytest.mark.ui
@allure.title("UI Test Login Fail")
def test_ui_loginfail(driver=setup_webdriver()):
    driver.get(API_BASE_URL + Login_Page)  # 打开登录页面
    find_element(driver,By.NAME, "email").send_keys("jun@vivalink.com.cn")
    find_element(driver,By.NAME, "password").send_keys("Jun@1234567")
    find_element(driver,By.CLASS_NAME, 'ant-btn').click()
    time.sleep(1)
    interfaces=filter_requestWillBeSent(driver)
    ele="ant-alert-message"

    #断言1 提示登陆失败
    try:
        alert = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, ele))).text
        logger.info(f"Alert is: {alert}")
        assert_in("Invalid Email or Password",alert,"Alert is not equal\n")
    finally:
        pass

    # print(321,interfaces)

    # 断言2 接口返回登陆失败
    try:
        for i in interfaces:
            if "/backend/authentication" in i.get("interface"):
                # logger.info(f"接口获取到的登陆Email: {i.get('request').get('data').get('email')}")
                with pytest.raises(AssertionError):
                    logger.info(f"接口请求: {i.get('request')}")
                    logger.error(f"登陆失败，接口返回: {i.get('response')}")
                    assert_equal(i.get("response").get("code"), 200, "email is not equal\n")

    finally:
        driver.quit()

