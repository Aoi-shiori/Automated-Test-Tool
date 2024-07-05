# common/config.py

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
# nginx_dir = "..\\nginx-1.21.0\\"
nginx_dir = "D:/01-WorkSpace/01-Code/01-Python/Automated Testing/nginx-1.27.0"

# Allure Report
def get_section_ALLURE_REPORT_CUSTOM(custom):

    customs = {
        "title": "Vivalink Webportal Report",
        "LogoFile": "../static/imgs/favicon.ico",
        "reportFilePath": "D:/01-WorkSpace/01-Code/01-Python/Automated Testing/reports/allure_reports_html",
        "allureFilePath": "D:/01-WorkSpace/01-Code/01-Python/Automated Testing/allure-2.29.0",
        "allureResultsPath": "D:\\01-WorkSpace\\01-Code\\01-Python\\Automated Testing\\reports\\allure_reports",
        "logoText": "Report",
        "reportContentTitle": "WebPortal v2.7 Report",
        "BaseUrl": API_BASE_URL
    }

    allure_report_custom = customs[custom]

    return allure_report_custom

