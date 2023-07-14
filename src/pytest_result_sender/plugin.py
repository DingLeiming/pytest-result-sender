from datetime import datetime, timedelta

import pytest
import requests

data = {
    "passed": 0,
    "failed": 0,
}


def pytest_runtest_logreport(report: pytest.TestReport):
    if report.when == "call":
        data[report.outcome] += 1


def pytest_collection_finish(session: pytest.Session):
    data["total"] = len(session.items)
    print("用例总数:", data["total"])


def pytest_configure():
    # 配置加载完毕执行，测试用例执行之前执行
    data["start_time"] = datetime.now()
    print(f"{datetime.now()}pytest开始执行了")


def pytest_unconfigure():
    # 配置加载完毕之后执行，测试用例执行之后执行
    data["end_time"] = datetime.now()
    print(f"{datetime.now()}pytest执行结束了")

    data["duration"] = data["end_time"] - data["start_time"]
    print(data["duration"])
    # assert timedelta(seconds=3) >= data['duration'] > timedelta(seconds=1.5)
    # assert data['total'] == 3
    # assert data['passed'] == 2
    # assert data['failed'] == 1

    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ebee6bbe-d60f-4db6-9c6d-ed03caa38429"
    content = (
        f"""
    pytest自动化测试结果

    测试时间：{data['end_time']} </br>
    用例数量：{data['total']} </br>
    执行时长：{data['duration']} </br>
    测试通过：<font color = 'green'>{data['passed']}</font> </br>
    测试失败：<font color = 'red'>{data['failed']}</font>
    """
        ""
    )
    requests.post(url, json={"msgtype": "markdown", "markdown": {"content": content}})
