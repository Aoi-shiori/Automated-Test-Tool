import subprocess
import time

import psutil
from common.logger import logger as logs
from common import config as conf
from util.getIP import get_local_ip
from pathlib import Path


class Nginx:
    def __init__(self):
        self.nginx_dir = conf.nginx_dir
        self.process_name = "nginx.exe"

    def dosomething(self):
        if self.process_exists(process_name=self.process_name):
            self.cd_nginx_dir()
            self.stop_nginx()
            self.start_nginx()
            self.restart_nginx()
            # 端口固定为8112，可以在ningx.conf中修改
            logs.info(f"Nginx Allure报告服务地址：http://{get_local_ip()}:8112")
        else:
            self.cd_nginx_dir()
            self.start_nginx()
            time.sleep(2)
            if self.process_exists(process_name=self.process_name):
                logs.info(f"Nginx Allure报告服务地址：http://{get_local_ip()}:8112")
            else:
                logs.error("Nginx服务启动失败，请检查Nginx配置或者Nginx是否安装")

    def process_exists(self, process_name):

        # 转换进程名为小写，因为psutil通常会返回小写的进程名
        process_name = process_name.lower()
        for proc in psutil.process_iter(['name']):
            try:
                # 过滤出匹配进程名的进程
                if proc.info['name'].lower() == process_name:
                    return True
            except psutil.NoSuchProcess:
                pass
        return False

    def cd_nginx_dir(self):
        logs.info("切换到Nginx目录...")
        # 运行一个Bash命令
        command = f"cd {self.nginx_dir}"
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logs.info("已切换到Nginx目录...")

    def start_nginx(self):
        # cwd=Path.cwd()
        # # logs.info("当前工作目录是1：",cwd)
        # print(1,cwd)
        # self.cd_nginx_dir()
        # cwd=Path.cwd()
        # # logs.info("当前工作目录是2：",cwd)
        # print(2,cwd)
        # cwd=cwd.joinpath(cwd.parent.parent,"nginx-1.20.1\\")
        # print(3,cwd)
        # # 运行一个Bash命令
        subprocess.run("start.bat",cwd=self.nginx_dir,shell=True, text=True)
        logs.info("Nginx服务启动中...")


    def stop_nginx(self):
        logs.info("停止Nginx服务...")

        # 运行一个Bash命令
        command = "nginx -s stop"
        subprocess.run(command,cwd=self.nginx_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logs.info("Nginx服务已停止...")

    def restart_nginx(self):
        logs.info("重启Nginx服务...")

        # 运行一个Bash命令
        command = "nginx -s reload"
        subprocess.run(command,cwd=self.nginx_dir,  shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logs.info("Nginx服务已重启...")

if __name__ == '__main__':
    nginx = Nginx()
    # exists=nginx.process_exists(process_name=nginx.process_name)
    # print(exists)
    nginx.dosomething()