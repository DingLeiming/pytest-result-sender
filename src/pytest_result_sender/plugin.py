from datetime import datetime, timedelta

import pytest
import requests

data = {
    "passed": 0,
    "failed": 0,
}


def pytest_addoption(parser):
    parser.addini(
        'send_when',
        help="何时发送结果？"

    )
    parser.addini(
        'send_api',
        help="发往何处?"

    )


def pytest_runtest_logreport(report: pytest.TestReport):
    if report.when == "call":
        data[report.outcome] += 1


def pytest_collection_finish(session: pytest.Session):
    data["total"] = len(session.items)
    print("用例总数:", data["total"])


def pytest_configure(config: pytest.Config):
    # 配置加载完毕执行，测试用例执行之前执行
    data["start_time"] = datetime.now()
    print(f"{datetime.now()}pytest开始执行了")
    data["send_when"] = config.getini("send_when")
    data["send_api"] = config.getini("send_api")


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
    send_result()


def send_result():
    if not data["send_api"]:
        return
    if data["send_when"] == 'never':
        return
    if data["send_when"] == 'on_fail' and data["failed"] == 0:
        return
    url = data["send_api"]
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
    try:
        requests.post(url, json={"msgtype": "markdown", "markdown": {"content": content}})
    except Exception:
        pass

    data['send_done'] = 1  # 发送成功
