# -*- coding: utf-8 -*-
# @Time  : 2024-7-4 21:46:28
# @Author: 郭军
# @Email:391350540@qq.com
# @File  : login.py
# @description:登陆测试case
# @Software: PyCharm
# @PythonVersion: python 3.12
# @Version : V1.0
# @Project: webportal
# @Description: 登陆页面case
# @Update: 2024-7-4 21:46:28
# @UpdateContent:  登陆页面case    x


import allure
import pytest
from selenium.webdriver.common.by import By

from common.helpers import assert_in, assert_equal
from common.logger import logger
from pages.login import LoginPage


@pytest.mark.env(test="dev")
@allure.epic("Webportal Login")
@allure.feature("Login")
@allure.title("UI Test Login")
@allure.story("测试登陆功能")
@allure.severity(allure.severity_level.CRITICAL)
class TestLogin:
    def setup_class(self):
        # 初始化页面 可以传入用户名和密码
        # self.login_page = LoginPage(user="111", password="333")

        # 初始化页面  如果不传入用户名和密码，则使用默认的用户名和密码
        self.login_page = LoginPage()

    def teardown_class(self):
        self.login_page.quit()
        pass


    @allure.title("UI Test Login Fail")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://kdocs.cn/l/cfye518QJFc8", name="用例文档")
    @allure.issue("https://kdocs.cn/l/cfye518QJFc8", name="问题链接")
    @allure.description("用户名是否是邮箱")
    @allure.severity(allure.severity_level.CRITICAL)  # 用例等级（blocker critical normal minor trivial）
    @allure.story("输入非邮箱格式的用户名，登录失败,提示用户名必须是有效的电子邮件地址")
    @pytest.mark.parametrize("username,passwd", [("999", "Jun@1234"), ("jun@vivalink.com.cn1", "999")])
    @pytest.mark.xfail #  预期失败：
    @pytest.mark.run(order=1)
    def test_login_userisemail(self, username, passwd):
        with allure.step("Open login page"):
            self.login_page.open("/sign-in")
        with allure.step("Login"):
            # 自定义用户名
            self.login_page.username = username
            self.login_page.name_imput()
        with allure.step("Input password"):
            self.login_page.userpasswd = passwd
            self.login_page.passwd_imput()
        with allure.step("Click submit"):
            self.login_page.click_submit()
        with allure.step("Check login fail"):
            isemail = self.login_page.find_element((By.CLASS_NAME, "ant-form-item-explain-error")).text
        assert_in("This field must be valid email", isemail)
        logger.info(f"Expected login failure, required prompt is：,{isemail}")


    @allure.title("UI Test Login Fail")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://kdocs.cn/l/cfye518QJFc8", name="用例文档")
    @allure.issue("https://kdocs.cn/l/cfye518QJFc8", name="问题链接")
    @allure.description("异常登录测试")
    @allure.severity(allure.severity_level.CRITICAL)  # 用例等级（blocker critical normal minor trivial）
    @allure.story("输入错误email和密码，登录失败,提示用户名或密码无效")
    @pytest.mark.parametrize("username,passwd", [("123@167.com", "Jun@1234"), ("jun@vivalink.com.cn", "999")])
    @pytest.mark.xfail  # 预期失败：
    @pytest.mark.run(order=2)
    def test_login_userfail(self, username, passwd):
        with allure.step("Open login page"):
            self.login_page.open("/sign-in")
        with allure.step("Login"):
            # 自定义用户名
            self.login_page.username = username
            self.login_page.name_imput()
        with allure.step("Input password"):
            self.login_page.userpasswd = passwd
            self.login_page.passwd_imput()
        with allure.step("Click submit"):
            self.login_page.click_submit()
        with allure.step("Check message"):
            message = self.login_page.wait_for_element((By.CLASS_NAME, "ant-alert-message")).text

        assert_in("Invalid Email or Password", message, "Alert is not equal\n")
        logger.info(f"Expected login failure, required prompt message is：,{message}")


    @allure.title("UI Test Login Success")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://kdocs.cn/l/cfye518QJFc8", name="用例文档")
    @allure.issue("https://kdocs.cn/l/cfye518QJFc8", name="问题链接")
    @allure.description("正常登录测试")
    @allure.severity(allure.severity_level.CRITICAL)  # 用例等级（blocker critical normal minor trivial）
    @allure.story("输入正确email和密码，登录成功,提示登陆成功")
    @pytest.mark.run(order=3)
    def test_login(self):
        with allure.step("Open login page"):
            self.login_page.open("/sign-in")
        with allure.step("Login"):
            # 自定义用户名
            self.login_page.username = "jun@vivalink.com.cn"
            self.login_page.name_imput()
        with allure.step("Input password"):
            self.login_page.userpasswd = "Jun@1234"
            self.login_page.passwd_imput()
        with allure.step("Click submit"):
            self.login_page.click_submit()
        assert_in("Program Manager Management", self.login_page.get_title())

        with allure.step("Get email"):
            email_path = '//*[@id="root"]/div/div/div/div/div/div/main/div/div/div[2]/div[2]/div/div/div/div/div/div/div/table/tbody/tr/td[4]'
            email_locate = (By.XPATH, email_path)
            email = self.login_page.find_element(email_locate).text

        with allure.step("get network,check login email"):
            interfaces = self.login_page.get_network(self.login_page.driver)
            try:
                for i in interfaces:
                    if "backend/currentUserInfo/" in i.get("interface"):
                        logger.info(f"接口获取到的登陆Email: {i.get("response").get("email")}")
                        assert_equal(i.get("response").get("email"), email, "email is not equal\n")
            finally:
                pass

        # 退出登录
        self.login_page.logout()
