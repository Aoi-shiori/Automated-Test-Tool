# -*- coding: utf-8 -*-
# @Time  : 2024-7-4 21:46:28
# @Author: 郭军
# @Email:391350540@qq.com
# @File  : allureUtil.py
# @Software: PyCharm
# @PythonVersion: python 3.12
# @Version : V1.0
# @Project: Automated Testing
# @Description: allureUtil
# @Update: 2024-7-17 08:49:49
# @UpdateContent:  allureUtil
import json
import os
import re
import shutil
from os import replace
import platform
import pytest

from common.logger import logger as logs
from common import  config as conf
from util.dircheck import check_dir as dir_check
from util.getIP import get_local_ip
from common.config import Port

class allureUtil:
    def __init__(self):
        self.title = conf.get_section_ALLURE_REPORT_CUSTOM("title") #
        self.LogoFile = conf.get_section_ALLURE_REPORT_CUSTOM("LogoFile")
        self.reportFilePath = conf.get_section_ALLURE_REPORT_CUSTOM("reportFilePath")
        self.logoText = conf.get_section_ALLURE_REPORT_CUSTOM("logoText")
        self.reportContentTitle = conf.get_section_ALLURE_REPORT_CUSTOM("reportContentTitle")
        self.allureFilePath = conf.get_section_ALLURE_REPORT_CUSTOM("allureFilePath")

    def doAllureCustom(self):
        self.replaceWebSiteTitle()
        self.replaceReportContentPageTitle()
        self.replaceFavicon()
        self.replaceLogosvg()
        self.replacelogoText()

    def replacelogoText(self):
        #图标右侧的展示文案
        # 获取CSS文件的路径
        Css_filepath = self.reportFilePath + r"/plugin/custom-logo/styles.css"
        try:
            file = open(Css_filepath, 'r', encoding="utf-8")
            content = file.read()

            oldText = re.search('content: "(.*?)";', content)
            if oldText is None:
                file.close()
                with open(Css_filepath, 'a',encoding="UTF-8") as file:
                    file.write('\n')
                    file.write(".side-nav__brand span{\n")
                    file.write("  display: none;\n")
                    file.write("}\n")
                    file.write(".side-nav__brand:after{\n")
                    file.write("  content: \"" + self.logoText + "\";\n")
                    file.write("  margin-left: 74px;\n")
                    file.write("}\n")
                    file.write(".side-nav__brand{\n")
                    file.write("    font-size: 16px;\n")
                    file.write("    font-weight: 450;\n")
                    file.write("    color: #fff;\n")
                    file.write("    margin-left: 5px;\n")
                    file.write("    line-height: 40px;\n")
                    file.write("}\n")

                file.close()
            else:
                oldText = oldText.group(1)
                content = content.replace(f"content: \"" + oldText, f"content: \"" + self.logoText)
                file.close()

                file = open(Css_filepath, 'w', encoding="utf-8")
                file.write(content)
        except Exception as e:
            logs.error(f'获取【{Css_filepath}】文件数据时出现未知错误: {str(e)}')
        finally:
            file.close()

    # 替换favicon.ico文件
    def replaceFavicon(self):
        # 定义源文件和目标目录
        target_Favicon_filepath = self.reportFilePath + r"/"
        source_Favicon_filepath = self.LogoFile
        shutil.copy2(source_Favicon_filepath, target_Favicon_filepath)

    # 替换logo.svg文件
    def replaceLogosvg(self):
        # 定义源文件和目标目录
        # target_Logosvg_filepath = self.reportFilePath + r"/plugin/custom-logo/"
        target_Logosvg_filepath = self.reportFilePath + r"/plugin/custom-logo/"
        # source_Logosvg_filepath = r"../static/imgs/custom-logo.svg"
        source_Logosvg_filepath = r"./static/imgs/custom-logo.svg"

        # 使用shutil.copy2()函数复制文件到目标目录并覆盖已存在的文件
        shutil.copy2(source_Logosvg_filepath, target_Logosvg_filepath)

    # 替换报告内容页面的标题
    def replaceReportContentPageTitle(self):
        # 获取文件的路径
        report_filepath = self.reportFilePath + r"/widgets/summary.json"
        try:
            file = open(report_filepath, 'r', encoding="utf-8")
            content = file.read()
            contentJson = json.loads(content)
            contentJson["reportName"] = self.reportContentTitle
            file.close()

            content = json.dumps(contentJson, ensure_ascii=False)
            file = open(report_filepath, 'w', encoding="utf-8")
            file.write(content)
        except Exception as e:
            logs.error(f'获取【{report_filepath}】文件数据时出现未知错误: {str(e)}')
        finally:
            file.close()

    # 替换网站标题
    def replaceWebSiteTitle(self):
        #获取HTML测试报告的路径
        report_filepath = self.reportFilePath + r"/index.html"
        try:
            file = open(report_filepath,'r',encoding="utf-8")
            content = file.read()
            #替换web页面的标题
            oldTitle = re.search("<title>(.*?)</title>", content)
            oldTitle = oldTitle.group(1)
            content = content.replace(f"<title>" + oldTitle,f"<title>" + self.title)
            file.close()

            file = open(report_filepath, 'w', encoding="utf-8")
            file.write(content)
        except Exception as e:
            logs.error(f'获取【{report_filepath}】文件数据时出现未知错误: {str(e)}')
        finally:
            file.close()

    # 替换allure.yml文件
    def replaceAllureconfig(self):
        # 获取文件的路径
        allureconfig_filepath = self.allureFilePath + r"/config/allure.yml"
        try:
            file = open(allureconfig_filepath, 'r', encoding="utf-8")
            content = file.read()
            text=re.search("- custom-logo-plugin",content)
            if text is None:
                file.close()
                with open(allureconfig_filepath, 'a', encoding="UTF-8") as file:
                    file.write('\n')
                    file.write("  - custom-logo-plugin\n")

            file.close()
        except Exception as e:
            logs.error(f'获取【{allureconfig_filepath}】文件数据时出现未知错误: {str(e)}')
        finally:
            file.close()


class allureUtil_SetEnv:
    def __init__(self):
        self.allureResultsPath = conf.get_section_ALLURE_REPORT_CUSTOM("allureResultsPath")
        self.allureFilePath = conf.get_section_ALLURE_REPORT_CUSTOM("allureFilePath")
        self.reportFilePath = conf.get_section_ALLURE_REPORT_CUSTOM("reportFilePath")
        self.title = conf.get_section_ALLURE_REPORT_CUSTOM("title")
        self.logoText = conf.get_section_ALLURE_REPORT_CUSTOM("logoText")
        self.reportContentTitle = conf.get_section_ALLURE_REPORT_CUSTOM("reportContentTitle")
        self.BaseUrl = conf.get_section_ALLURE_REPORT_CUSTOM("BaseUrl")

    def doAllureCustom(self):
        self.set_report_env_on_results()
        self.set_report_executer_on_results()

    def set_report_env_on_results(self):
        """
        在allure-results报告的目录下生成一个写入了环境信息的文件：environment.properties(注意：不能放置中文，否则会出现乱码)
        @return:
        """
        # 需要写入的环境信息
        allure_env = {
            'OperatingEnvironment': "Test Environment",
            'BaseUrl': self.BaseUrl,
            'PythonVersion': platform.python_version(),
            'Platform': platform.platform(),
            'PytestVersion': pytest.__version__,
            "reportUrl": f"http://{get_local_ip()}:{Port}",

        }


        allure_env_file = os.path.join(self.allureResultsPath, 'environment.properties')


        with open(allure_env_file, 'w', encoding='utf-8') as f:
            for _k, _v in allure_env.items():
                f.write(f'{_k}={_v}\n')


    def set_report_executer_on_results(self):
        """
        在allure-results报告的目录下生成一个写入了执行人的文件：executor.json
        @return:
        """
        # 需要写入的环境信息
        allure_executor = {
            "name": "郭军",
            "type": "jenkins",
            "url": f"http://{get_local_ip()}:{Port}",  # allure报告的地址
            "buildOrder": 3,
            "buildName": "allure-report_deploy#1",
            "buildUrl": "https://jenkins.vivalink.com.cn/#1",
            "reportUrl": f"http://{get_local_ip()}:{Port}",
            "reportName": "郭军 Allure Report"
        }
        allure_env_file = os.path.join(self.allureResultsPath, 'executor.json')
        with open(allure_env_file, 'w', encoding='utf-8') as f:
            f.write(str(json.dumps(allure_executor, ensure_ascii=False, indent=4)))
if __name__ == '__main__':
    allure = allureUtil()
    # allure.doAllureCustom()
    # allureUtil_SetEnv = allureUtil_SetEnv()
    # allureUtil_SetEnv.doAllureCustom()
    allure.replaceFavicon()
    print("Allure报告定制完成")