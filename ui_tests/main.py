# -*- coding: utf-8 -*-
# @Time  : 2024-7-4 21:46:28
# @Author: 郭军
# @Email:391350540@qq.com
# @File  : main.py
# @Software: PyCharm
# @PythonVersion: python 3.12
# @Version : V1.0
# @Project: webportal
# @Description: main函数
# @Update: 2024-7-5 10:57:52
# @UpdateContent:  main函数

import os

import pytest
from common.createReport import setup_allure_Report_server
from common.nginx import Nginx
from util.allureUtil import allureUtil, allureUtil_SetEnv
from common.config import Port
from common.logger import logger

if __name__ == '__main__':
    logger.info(f"{"*"*20}开始执行测试用例{"*"*20}")
    pytest.main(["-s", "-v", "--alluredir=../reports/allure_reports", "--clean-alluredir"])

    # 设置环境信息
    allureUtil_SetEnv = allureUtil_SetEnv()
    allureUtil_SetEnv.doAllureCustom()

    # 生成报告
    os.system("allure generate ../reports/allure_reports -o ../reports/allure_reports_html --clean")

    # 生成报告后，自定义报告
    allure = allureUtil()
    allure.doAllureCustom()

    # 启动零时Allure报告服务--正式环境需要使用Nginx或者Jenkins
    # setup_allure_Report_server(Port)

    # 启动nginx Allure报告服务
    nginx = Nginx()
    nginx.dosomething()
    logger.info(f"{"*"*20}测试用例执行完成{"*"*20}")