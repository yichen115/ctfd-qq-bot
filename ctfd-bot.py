# -*- coding: utf-8 -*-  
from bs4 import BeautifulSoup
import re,json,time,configparser,logging,sys,os,requests,asyncio

my_headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip',
        'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
    }
############自定义参数#############
ctfd_url = 'http://ip:port'       #这里填写ctfd的地址
username = "xxxx"                 #ctfd账户
password = "xxxx"                 #ctfd密码
qq_group = "xxxxxxx"              #qq群号
############自定义参数#############
login_url = ctfd_url + '/login'
apiusers = ctfd_url + '/api/v1/users'
apisubs = ctfd_url + '/api/v1/submissions'
group_api = "http://127.0.0.1:5700/send_group_msg?group_id="+ qq_group +"xxx&message="
#这个地址是go-cqhttp默认的

sss = requests.Session()
r = sss.get(login_url, headers = my_headers)

#获取csrfNonce,不会写正则，麻烦了点
soup = BeautifulSoup(r.text,"html.parser")
script = soup.find("script")
index = str(script).find("csrfNonce")
csrfNonce = str(script)[index+13:index+13+64]

my_data = {
'name' : username,
'password' : password,
'_submit' : 'Submit',
'nonce' : csrfNonce,
}

#login
try:
  r = sss.post(login_url, headers = my_headers, data = my_data)
except:
  print('[error]fail to login,check your config and network')
if r.ok == True:
  print('[success]login ok,start the robot...')
else:
  pass

#获取用户列表
def get_user_list():
    apiUrl = apiusers
    try:
        responseJson = sss.get(apiUrl, headers = my_headers)
    except:
        print('[error]fail to get api info,continue.')
        return []
    jsonInfo = json.loads(responseJson.text)
    if jsonInfo['success'] != True:
        print("error to get userlist")
        return []
    userList = eval(str(jsonInfo['data']))
    return userList

#获取提交flag信息
def get_attempt_info():
    apiUrl = apisubs #ctfd地址
    try:
        responseJson = sss.get(apiUrl, headers = my_headers)
    except:
        print('[error0]fail to get api info,continue.')
        return []
    jsonInfo = json.loads(responseJson.text)
    if jsonInfo['success'] != True:
        print("error to get attemptlist")
        return []
    allList = eval(str(jsonInfo['data']))
    return allList

#异步循环发送请求
async def deal_user_list():
    global userLen,userList
    while True:
        try:
            tmpList = get_user_list()
            tmpLen = len(tmpList)
            print(userLen,tmpLen)
            if tmpLen == 0:
                await asyncio.sleep(3)
                continue
            if userLen < tmpLen:
                for i in range(userLen,tmpLen):
                    message = "新用户"+tmpList[i]['name']+"成功注册~"
                    print(message)
                    requests.get(group_api+message)
                userLen = tmpLen
                userList = tmpList
            else:
                userLen = tmpLen
                userlist = tmpList
            await asyncio.sleep(3)
        except TypeError:
            print('[error1]fail to get api info,continue.')
            continue
            await asyncio.sleep(3)

async def deal_attemp_list():
    global userLen,userList,allLen,allList
    while True:
        try:
            tmpallList = get_attempt_info()
            tmpallLen = len(tmpallList)
            if tmpallLen == 0:
                await asyncio.sleep(3)
                continue
            if allLen < tmpallLen:
                for i in range(allLen,tmpallLen):
                    if tmpallList[i]['type'] == "correct":
                        chaname = ""
                        for s in userList:
                            if str(s['id']) == str(tmpallList[i]['user_id']):
                                chaname = s['name']
                                if chaname == "":
                                    continue
                                    await asyncio.sleep(3)
                        message = "恭喜" + chaname + "做出" + str(tmpallList[i]['challenge']['category'])+"题目：" + str(tmpallList[i]['challenge']['name'])
                        print(message)
                        requests.get(group_api+message)
                allLen = tmpallLen
                allList = tmpallList
            else:
                allLen = tmpallLen
                allList = tmpallList
            await asyncio.sleep(3)
        except TypeError:
            print('[error2]fail to get api info,continue.')
            continue         

if __name__ == ("__main__"):
    logging.basicConfig(filename='err.log',level=logging.ERROR,format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',datefmt='%Y-%m-%d')
    userList = get_user_list()
    #userLen = 0
    userLen = len(userList)
    allList = get_attempt_info()
    allLen = len(allList)
    #allLen = 0
    loop = asyncio.get_event_loop()
    tasks = [deal_user_list(),deal_attemp_list()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()