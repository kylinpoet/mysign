import requests
import json

from config import *


def message2dingtalk2(content):
    global sign_web
    if sign_web is None:
        sign_web = ''
    
    ding_access_token = "b84b446682f1348a162a0e3f09f935ea902e7a07d088fd5ade45a18a8b9df878"
    url = f'https://oapi.dingtalk.com/robot/send?access_token={ding_access_token}'
    secret = f'{sign_web}-ohwgy-签到：'
    headers={
        "Content-Type": "application/json"
            }
    data={"msgtype": "text",
            "text": {
                 "content": secret + content
            }
          }
    json_data=json.dumps(data)
    requests.post(url=url,data=json_data,headers=headers)

def main():

    url = "https://api.dfrobot.com.cn/user/login"

    headers = {
        "Host": "api.dfrobot.com.cn",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
    }

    post_info = f'{{"password":"{password}","email":"{email}"}}'
    payload = {
        "biz_content": post_info,
        "sign_type": "md5",
        "sign": sign,
        "timestamp": "1693747152564",
        "version": "1",
    }

    response = requests.post(url, headers=headers, data=payload)

    try:
        if response.status_code == 200:
            # print("HTTP POST请求成功，响应内容如下:")
            app_auth_token = response.json()['data']['app_auth_token']

            # reqSession = requests.Session()
            url = f"https://mcmobileapi.dfrobot.com.cn/user_api.php?token={app_auth_token}"
            headers = {
                        "Host": "mcmobileapi.dfrobot.com.cn",
                        "Accept": "application/json, text/plain, */*",
                        "Sec-Ch-Ua-Mobile": "?0",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
                        "Accept-Encoding": "gzip, deflate",
                    }
            response = requests.get(url, headers=headers).json()
            uid = response['uid']
            hash = response['hash']
            group = response['group'].replace('<font color="#9966FF">','').replace('</font>','')
            credits = response['credits']
            extcredits4 = response['extcredits4']
            print(f"积分：{credits}，创造力：{extcredits4}，称号：{group}")
            
            WebKitFormBoundary1rBsa0cRykASJXtY = f"""------WebKitFormBoundary1rBsa0cRykASJXtY
    Content-Disposition: form-data; name="formhash"

    {hash}
    ------WebKitFormBoundary1rBsa0cRykASJXtY
    Content-Disposition: form-data; name="qdxq"

    wc
    ------WebKitFormBoundary1rBsa0cRykASJXtY
    Content-Disposition: form-data; name="qdmode"

    2
    ------WebKitFormBoundary1rBsa0cRykASJXtY
    Content-Disposition: form-data; name="todaysay"

    from python
    ------WebKitFormBoundary1rBsa0cRykASJXtY
    Content-Disposition: form-data; name="id"

    {uid}

    """
            url = "https://mc.dfrobot.com.cn/user_api.php?act=sign"
            headers = {
                        "Host": "mc.dfrobot.com.cn",
                        "Accept": "application/json, text/plain, */*",
                        # "Content-Type": "multipart/form-data",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
                        "Referer": "https://mc.dfrobot.com.cn/forum.html",
                        "Accept-Encoding": "gzip, deflate",
                        }

            data = {
                "formhash": (None, hash),
                "qdxq": (None, "wc"),
                "qdmode": (None, "2"),
                "todaysay": (None, "From Python"),
                "id": (None, uid),
            }
            response = requests.post(url, headers=headers, files=data).json()
            print(response['message'])
            message2dingtalk2(f"签到成功,签到前：积分：{credits}，创造力：{extcredits4}，称号：{group}")
            return '签到消息发送成功！'
        else:
            print(f"HTTP POST请求失败，状态码: {response.status_code}")
            message2dingtalk2(f'{response.text}')
            return '签到失败'
    except Exception as e:
        print(str(e))
        message2dingtalk2(str(e))
        return '签到错误'


def handler(event, context):
    return main()


if __name__ == '__main__':
    main()