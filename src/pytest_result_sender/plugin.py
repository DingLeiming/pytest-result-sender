from datetime import datetime


# 配置加载完毕执行，测试用例执行之前执行
def pytest_configure():
    print(f"{datetime.now()}pytest开始执行了")


def pytest_unconfigure():
    print(f"{datetime.now()}pytest执行结束了")
