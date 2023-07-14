import requests

url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ebee6bbe-d60f-4db6-9c6d-ed03caa38429"
content = (
    """
pytest自动化测试结果

测试时间：XXX-XXXX-XX </br>
用例数量：100 </br>
执行时长：50s </br>
测试通过：<font color = 'green'>2</font> </br>
测试失败：<font color = 'red'>1</font>
"""
    ""
)
requests.post(url, json={"msgtype": "markdown", "markdown": {"content": content}})
