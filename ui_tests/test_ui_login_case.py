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
import time

import allure
import pytest
from selenium.webdriver.common.by import By
from common.helpers import assert_in, assert_equal, assert_is_instance
from common.logger import logger
from pages.login import LoginPage


@pytest.mark.env(test="dev")
@allure.epic("Webportal Login Page")
@allure.feature("Login(登陆功能测试)")
@allure.title("UI Test Login")
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
    @allure.link("https://kdocs.cn/l/cfye518QJFc8?linkname=3", name="用例链接")
    # @allure.issue("https://kdocs.cn/l/cfye518QJFc8", name="问题链接")
    @allure.severity(allure.severity_level.CRITICAL)  # 用例等级（blocker critical normal minor trivial）
    @allure.story("CaseID：20250627140641 -> 测试非邮箱用户名登录") #标题
    @allure.description("ID: 20250627140641 \r"
                  "标题：测试非邮箱用户名登录 \r"
                  "前置：1、进入登录页面 \r"
                  "步骤：1、输入非邮箱格式的用户名进行登录 \r"
                  "预期：1、登陆失败，提示用户名必须是有效的电子邮件地址:“This field must be valid email”")#描述信息

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
    @allure.link("https://kdocs.cn/l/cfye518QJFc8?linkname=2", name="用例链接")
    # @allure.issue("https://kdocs.cn/l/cfye518QJFc8", name="问题链接")
    @allure.severity(allure.severity_level.CRITICAL)  # 用例等级（blocker critical normal minor trivial）
    @allure.story("CaseID：20250627140641 -> 测试错误的邮箱密码登录")
    @allure.description("ID: 20250627113128 \r"
                  "标题：测试错误的邮箱密码登录 \r"
                  "前置：1、进入登录页面 \r"
                  "步骤：1、输入错误email和密码进行登录 \r"
                  "预期：1、登陆失败，提示用户名或者密码无效：“invalid Email or Password”")

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

        assert_in("invalid Email or Password", message, "Alert is not equal\n")
        logger.info(f"Expected login failure, required prompt message is：,{message}")


    @allure.title("UI Test Login Success")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://kdocs.cn/l/cfye518QJFc8?linkname=1", name="用例链接")
    # @allure.issue("https://kdocs.cn/l/cfye518QJFc8", name="问题链接")
    @allure.severity(allure.severity_level.CRITICAL)  # 用例等级（blocker critical normal minor trivial）
    @allure.story("CaseID：20250627140626 -> 测试正常登录功能")
    @allure.description("ID: 20250627140626 \r"
                  "标题：测试正常登录功能 \r"
                  "前置：1、完成用户注册 \r"
                  "步骤：1、输入正确email和密码 \r"
                  "期望：可以正常登录，并提示登陆成功")
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
        assert_in("User Management", self.login_page.get_title())


        with allure.step("Get email"):
            email_class="ant-table-cell"
            email_locate = (By.CLASS_NAME, email_class)
            emails = self.login_page.find_elements(email_locate)

            e_text=[]
            for e in emails:
                e_text.append(e.text)

            email_list=[]
            for e in e_text:
                if "@" in e:
                    email_list.append(e)
            logger.info(f"找到当前Clinic用户列表: {email_list}")


        with allure.step("get network,check login email"):
            interfaces = self.login_page.get_network(self.login_page.driver)
            try:
                for i in interfaces:
                    if "backend/currentUserInfo/" in i.get("interface"):
                        logger.info(f"接口获取到的登陆Email: {i.get("response").get("email")}")
                        # assert_in(i.get("response").get("email"), email, "email is not equal\n")
                        assert i.get("response").get("email") in email_list,"找到Email"
                    else:
                        pass
            finally:
                pass

        # 退出登录
        self.login_page.logout()
