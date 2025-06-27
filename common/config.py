# common/config.py
import os

# 对于其他数据库，如 PostgreSQL、MySQL，连接字符串会有所不同
# PostgreSQL: 'postgresql://user:password@localhost/dbname'
# MySQL: 'mysql+pymysql://user:password@localhost/dbname'
# [Mysql]
# 替换以下信息为你的数据库连接信息

DATABASE_HOST = 'test-vcloud.cnibqlp0f4yv.ap-south-1.rds.amazonaws.com'
DATABASE_HOST = 'test-vcloud.cnibqlp0f4yv.ap-south-1.rds.amazonaws.com'
DATABASE_HOST = 'test-vcloud.cnibqlp0f4yv.ap-south-1.rds.amazonaws.com'
DATABASE_PORT = '3306'
DATABASE_USER = 'jun'
DATABASE_PASSWORD = 'VVadMmdoi78jasd2]'
# 构建连接URL
DB_CONNECTION_STRING = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/vcloud_test?charset=utf8mb4&connect_timeout=30000"

TEST_DB_CONNECTION_STRING_Vcloud = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/vcloud_test?charset=utf8mb4&connect_timeout=30000"
TEST_DB_CONNECTION_STRING_Vcloud_Static = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/vcloud_statistic_test?charset=utf8mb4&connect_timeout=30000"
PRESSURE_TEST_DB_CONNECTION_STRING_Vcloud_test = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/vcloud_statistic_test?charset=utf8mb4&connect_timeout=30000"



db_rul = {
    "dev" : [DB_CONNECTION_STRING,DB_CONNECTION_STRING],
    "Prod" : [DB_CONNECTION_STRING,DB_CONNECTION_STRING],
    "pressure": [DB_CONNECTION_STRING,DB_CONNECTION_STRING]
}


# API base URL
API_BASE_URL = "https://webportal-dev.vivalink.com"

# WebDriver path (for Selenium)
WEBDRIVER_PATH = "/path/to/chromedriver"

# 默认登陆账号密码
WebPortal_username = "jun@vivalink.com.cn"
WebPortal_password = "Jun@1234"

# Page URLs
Login_Page = "/sign-in"
User_Management_Page = "/user-management"
Rpm_Page = "/rpm/rt"
# 零时服务端口
Port = "8111"

def get_root_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


# nginx_dir = "../nginx-1.21.0/"
nginx_dir = f"{get_root_path()}/nginx-1.27.0"

# 获取根目录


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