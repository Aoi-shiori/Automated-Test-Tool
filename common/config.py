# common/config.py
import os

# 对于其他数据库，如 PostgreSQL、MySQL，连接字符串会有所不同
# PostgreSQL: 'postgresql://user:password@localhost/dbname'
# MySQL: 'mysql+pymysql://user:password@localhost/dbname'
# [Mysql]
# 替换以下信息为你的数据库连接信息
DATABASE_USER = 'jun'
DATABASE_PASSWORD = 'VVadMmdoi78jasd2]'
DATABASE_HOST = 'test-vcloud.cnibqlp0f4yv.ap-south-1.rds.amazonaws.com'
DATABASE_NAME = 'vcloud_test'
DATABASE_PORT = '3306'
# 构建连接URL
DB_CONNECTION_STRING = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}?charset=utf8mb4&connect_timeout=30000"



# API base URL
API_BASE_URL = "https://webportal-dev.vivalink.com"

# WebDriver path (for Selenium)
WEBDRIVER_PATH = "/path/to/chromedriver"

# 默认登陆账号密码
WebPortal_username = "jun@vivalink.com.cn"
WebPortal_password = "Jun@1234"

# Page URLs
Login_Page = "/sign-in"
User_Management_Page = "/user-management/pm-management"
Rpm_Page = "/rpm/rt"
# 零时服务端口
Port = "8111"
# nginx_dir = "../nginx-1.21.0/"
nginx_dir = "D:/01-WorkSpace/01-Code/01-Python/Automated Testing/nginx-1.27.0"

# 获取根目录
def get_root_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Allure Report
def get_section_ALLURE_REPORT_CUSTOM(custom):

    customs = {
        "title": "Vivalink Webportal Report",
        "LogoFile": "./static/imgs/favicon.ico",
        "reportFilePath": "./reports/allure_reports_html",
        "allureFilePath": "./allure-2.29.0",
        "allureResultsPath": "./reports/allure_reports",
        "logoText": "Report",
        "reportContentTitle": "WebPortal v2.7 Report",
        "BaseUrl": API_BASE_URL
    }

    allure_report_custom = customs[custom]

    return allure_report_custom