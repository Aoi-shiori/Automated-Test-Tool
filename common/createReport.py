import subprocess
from common.logger import logger as logs
from util.getIP import get_local_ip


def create_report():
    # # 运行一个Bash命令
    command = "allure serve ../reports/allure_reports"
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # command = ["allure generate  ../reports/allure_reports","-o ../reports/allure_reports_html","allure open ../reports/allure_reports_html"]
    # process2 = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # # 打印命令的输出和错误信息
    print(process.stdout)
    if process.stderr:
        print(process.stderr)



def setup_allure_Report_server(port):
    logs.info("启动Allure报告服务...")

    # 运行一个Bash命令
    # command = "allure serve ../reports/allure_reports"
    command=f"python -m http.server --directory ../reports/allure_reports_html {port}"
    logs.info(command)
    ip=get_local_ip()
    logs.info(f"启动Allure报告服务：http://{ip}:8111")
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 打印命令的输出和错误信息
    logs.info(process.stdout)

    if process.stderr:
        logs.info(process.stderr)
    url=f"http://localhost:{port}"
    return url