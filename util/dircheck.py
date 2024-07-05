import os


def check_dir(dir_path):
    """
    检查日志文件的父目录是否存在，不存在则创建
    """
    try:
        # 确保日志文件的父目录存在
        if not os.path.exists(os.path.dirname(dir_path)):
            os.makedirs(os.path.dirname(dir_path))
            return True
        else:
            return False
    except Exception as e:
        print(f"Failed to create log directory: {e}")