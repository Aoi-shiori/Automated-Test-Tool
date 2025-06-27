import time

import allure
import pytest

from pages.base import BasePage
from pages.rpm import RpmPage
from common.config import API_BASE_URL
from selenium.webdriver.common.by import By
from common.helpers import filter_requestWillBeSent, assert_in
from selenium.webdriver.common.action_chains import ActionChains
from common.logger import logger
from common.config import WebPortal_username,WebPortal_password
from common.Database import Database
@pytest.mark.env(test="dev")
@allure.epic("Webportal RPM")
@allure.feature("RPM")
@allure.story("UI Test RPM")
@allure.title("UI Test RPM")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.skip(reason="用例未调试好，暂不执行")
class TestRpm:
    def setup_class(self):

        # 初始化页面
        # 可以传入用户名和密码
        # self.rpm_page = RpmPage(user="111",password="333")

        # 如果不传入用户名和密码，则使用默认的用户名和密码
        self.rpm_page = RpmPage()


    def teardown_class(self):
        self.rpm_page.quit()

    @allure.title("UI Test RPM Last Upload Time")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://kdocs.cn/l/cfye518QJFc8",name="用例文档")
    @allure.issue("https://kdocs.cn/l/cfye518QJFc8",name="问题链接")
    @allure.description("check last upload time")
    @allure.severity(allure.severity_level.CRITICAL) # 用例等级（blocker critical normal minor trivial）
    @allure.story("传入subjectid参数，检查Last upload时间是否正确,如果没有数据则返回No data")
    @pytest.mark.parametrize("subjectid",["J001","999-777"])
    @pytest.mark.run(order=1)
    def test_rpm_last_upload_time(self,subjectid):
        with allure.step("Open login page"):
            self.rpm_page.open("/rpm/rt")
        with allure.step("Check Last upload"):
            Last_upload = self.rpm_page.get_rpm_user_last_upload_time(subjectid)
        if Last_upload == "No data":
            logger.info(f"用户:{subjectid}没有上传数据")
            with pytest.raises(AssertionError):

                assert_in("Last upload", Last_upload, "Last Upload is not equal\n")
        else:
            assert_in("Last upload", Last_upload, "Last Upload is not equal\n")
            logger.info(f"用户:{subjectid}的Last_upload是："+Last_upload)

    @allure.title("UI Test RPM SubjectID")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://kdocs.cn/l/cfye518QJFc8",name="用例文档")
    @allure.issue("https://kdocs.cn/l/cfye518QJFc8",name="问题链接")
    @allure.description("check subjectID")
    @allure.severity(allure.severity_level.CRITICAL) # 用例等级（blocker critical normal minor trivial）
    @allure.story("检查SubjectID是否正确")
    @pytest.mark.run(order=2)
    def test_rpm_subjectID(self):
        with allure.step("Open login page"):
            self.rpm_page.open("/rpm/rt")
        with allure.step("Check SubjectID"):
            subjectID = self.rpm_page.get_rpm_subjectID()
        assert_in("J001",subjectID,"SubjectID is not equal\n")
        logger.info(f"SubjectID is："+subjectID)
        with allure.step("Check Databases SubjectIDs"):
            db = Database()
            session = db.get_session()
            tables = db.get_tables("vcloud_user")
            subjectIDs = session.query(tables).filter(tables.user_name == subjectID).all()
            assert_in("J001",subjectIDs[0].subject_id,"SubjectID is not equal\n")

