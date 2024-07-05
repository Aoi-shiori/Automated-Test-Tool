import socket


def get_local_ip():
    """
    获取本地IP
    :return:
    """

    try:
        ip = socket.gethostbyname(socket.gethostname())
        return ip
    except Exception as e:
        print(e)
        return "localhost"

if __name__ == '__main__':
    print(get_local_ip())