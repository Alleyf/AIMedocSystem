# coding=<utf-8>
import json

import requests
from pypushdeer import PushDeer

pushdeer = PushDeer(pushkey="xxx")


def send_text(txt: str):
    try:
        return pushdeer.send_text(txt, desp="-智检慧医为您服务")
    except Exception as e:
        return e


def send_markdown(markdown):
    try:
        return pushdeer.send_markdown(markdown, desp="**-智检慧医为您服务**")
    except Exception as e:
        return e


def send_image(imgurl: str):
    try:
        return pushdeer.send_image(imgurl)
    except Exception as e:
        return e


def send_image_base64(img_base64: str):
    try:
        return pushdeer.send_image("data:image/png;base64," + img_base64)
    except Exception as e:
        return e


def news():
    i = 0
    url = 'http://excerpt.rubaoo.com/toolman/getMiniNews'
    r = requests.get(url)
    dic = json.loads(r.text)
    lt = dic['data']['news']
    for new in lt:
        new += '\n'
        lt[i] = new
        i += 1
    s = "".join(lt)
    return s


def wx_upload_file(filename):
    # 定义企业微信API的参数
    corpid = 'ww7c7fa044e0fd4516'  # 企业ID
    corpsecret = '9Y-Yk_AySfcYQaJdn1lgj8eS1XR2b7P5gQQwiEcEfXw'  # Secret

    res = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}")
    access_token = res.json()['access_token']
    url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload"
    params = {"access_token": access_token, "type": "file"}

    # 定义文件路径和文件名
    file_name = filename + ".pdf"
    print(file_name)
    file_path = "./media/docs/" + file_name  # 实际
    # file_path = "../../media/docs/" + file_name  # 测试

    # 打开文件并读取内容
    with open(file_path, "rb") as file:
        file_content = file.read()

    # 构造请求包中的文件信息
    files = {
        "media": (file_name, file_content, {
            "Content-Type": "multipart/form-data",
            "Content-Length": str(len(file_content))
        })
    }

    # 发送POST请求上传文件
    response = requests.post(url, params=params, files=files)

    # 输出返回结果
    # print(response.json())
    return response.json()['media_id']


def wx_send_file(media_id):
    userid = 'FanCaiSheng'  # userid
    agentid = '1000004'  # 应用ID
    corpsecret = '9Y-Yk_AySfcYQaJdn1lgj8eS1XR2b7P5gQQwiEcEfXw'  # Secret
    corpid = 'ww7c7fa044e0fd4516'  # 企业ID

    res = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}")
    access_token = res.json()['access_token']
    json_dict = {
        "touser": userid,
        "msgtype": "file",
        "agentid": agentid,
        "file": {
            "media_id": media_id
        },
        "safe": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    json_str = json.dumps(json_dict, separators=(',', ':'))
    res = requests.post(f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}", data=json_str)
    # print(res.json())
    return res.json()['errmsg'] == 'ok'


def wx_send_all_file(msg):
    userid = 'FanCaiSheng'  # userid
    agentid = '1000004'  # 应用ID
    corpsecret = '9Y-Yk_AySfcYQaJdn1lgj8eS1XR2b7P5gQQwiEcEfXw'  # Secret
    corpid = 'ww7c7fa044e0fd4516'  # 企业ID

    res = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}")
    access_token = res.json()['access_token']
    json_dict = {
        "touser": userid,
        "msgtype": "markdown",
        "agentid": agentid,
        "markdown": {
            "content": msg
        },
        "safe": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    json_str = json.dumps(json_dict, separators=(',', ':'))
    res = requests.post(f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}", data=json_str)
    # print(res.json())
    return res.json()['errmsg']


if __name__ == '__main__':
    # send_text("测试以下哦")
    # send_image(imgurl="https://s2.loli.net/2023/03/20/dC7PyWFI5ZmHhxr.png")
    # wx_upload_file(filename="2016IJC-导管组织接触对于模型的影响PentarRay_FAM")
    wx_send_file(media_id=wx_upload_file(filename="2016IJC-导管组织接触对于模型的影响PentarRay_FAM"))
