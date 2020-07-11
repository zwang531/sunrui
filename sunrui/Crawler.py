import requests
import zlib
import json
import base64
import time
import xlwt
from sunrui.Structure import Project, Record


def AddSalt(ori:bytearray):
    #从网页JS当中提取到的混淆盐值，每隔一位做一次异或运算
    Salt = '%#54$^%&SDF^A*52#@7'
    i = 0
    for ch in ori:
        if i%2==0:
            ch = ch ^ ord(Salt[(i//2) % len(Salt)])
        ori[i]=ch
        i+=1
    return ori

def EncodeData(ori:str):
    #开头的数字是原始报文长度
    Length = len(ori)
    Message = str.encode(ori)
    #首先用zlib进行压缩
    Compressed = bytearray(zlib.compress(Message))
    #然后加盐混淆
    Salted = AddSalt(Compressed)
    #最后将结果转化为base64编码
    Result = base64.b64encode(Salted).decode('utf-8')
    #将长度头和base64编码的报文组合起来
    return str(Length) + '$' + Result

def DecodeData(ori:str):
    #分离报文长度头
    #TODO: 增加报文头长度的验证
    Source = ori.split('$')[1]
    #base64解码
    B64back = bytearray(base64.b64decode(Source))
    #重新进行加盐计算，恢复原始结果
    Decompressed = AddSalt(B64back)
    #zlib解压
    Result = zlib.decompress(Decompressed).decode('utf-8')
    #提取json
    return json.loads(Result)

def SendRequest(url:str,data:str):
    Headers = {
        'Content-Type': 'application/json', 
        'Origin': 'https://www.tao-ba.club', 
        'Cookie': 'l10n=zh-cn', 
        'Accept-Language': 'zh-cn', 
        'Host': 'www.tao-ba.club', 
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15', 
        'Referer': 'https://www.tao-ba.club/', 
        'Accept-Encoding': 'gzip, deflate, br', 
        'Connection': 'keep-alive'
    }
    Data = EncodeData(data)
    Res = requests.post(url=url,data=Data,headers=Headers)
    ResText = Res.text
    return DecodeData(ResText)

def GetDetail(pro_id:int):
    #获得项目基本信息
    Data='{{"id":"{0}","requestTime":{1},"pf":"h5"}}'.format(pro_id,int(time.time()*1000))
    Response=SendRequest('https://www.tao-ba.club/idols/detail',Data)
    return Project(int(Response['datas']['id']),
        Response['datas']['title'],
        int(Response['datas']['start']),
        int(Response['datas']['expire']),
        float(Response['datas']['donation']),
        int(Response['datas']['sellstats'])
    )
#
# def GetPurchaseList(pro_id:int):
#     #获得所有人购买的数据，以list形式返回
#     Data='{{"ismore":false,"limit":15,"id":"{0}","offset":0,"requestTime":{1},"pf":"h5"}}'.format(pro_id,int(time.time()*1000))
#     Response=SendRequest('https://www.tao-ba.club/idols/join',Data)
#     Founderlist = []
#     Cleared = False
#     pages=0
#     while not Cleared:
#         for thisRecord in Response['list']:
#             Founderlist.append(Record(pro_id,
#                 int(thisRecord['userid']),
#                 thisRecord['nick'],
#                 float(thisRecord['money']),
#             ))
#         if len(Response['list']) == 15:
#             pages += 1
#             Data='{{"ismore":true,"limit":15,"id":"{0}","offset":{2},"requestTime":{1},"pf":"h5"}}'.format(pro_id,int(time.time()*1000),pages*15)
#             Response=SendRequest('https://www.tao-ba.club/idols/join',Data)
#         else:
#             Cleared = True
#     return Founderlist

def GetRecords(pro_id):
    # 获得项目基本信息
    Data = '{{"id":"{0}","requestTime":{1},"pf":"h5"}}'.format(pro_id, int(time.time() * 1000))
    Response = SendRequest('https://www.tao-ba.club/idols/detail', Data)

    return GetPurchaseList(pro_id, (int(Response['datas']['start'])), int(Response['datas']['expire']))


def GetPurchaseList(pro_id, startTime, endTime):
    # 获得所有人购买的数据，以list形式返回
    Data = '{{"ismore":false,"limit":15,"id":"{0}","offset":0,"requestTime":{1},"pf":"h5"}}'.format(pro_id, int(
        time.time() * 1000))
    Response = SendRequest('https://www.tao-ba.club/idols/join', Data)
    Founderlist = []
    Cleared = False
    pages = 0
    amountTotal = 0
    while not Cleared:
        for thisRecord in Response['list']:
            Founderlist.append(thisRecord)
            amountTotal += float(thisRecord['money'])
        while not Cleared:
            for thisRecord in Response['list']:
                Founderlist.append(thisRecord)
                amountTotal += float(thisRecord['money'])
                if(float(thisRecord['money'])>1000):
                    distribution['大于1000'] = distribution['大于1000']+1
                elif(float(thisRecord['money'])>501):
                    distribution['501-1000'] = distribution['501-1000']+1
                elif(float(thisRecord['money'])>101):
                    distribution['101-500'] = distribution['101-500']+1
                elif(float(thisRecord['money'])>51):
                    distribution['51-101'] = distribution['51-101']+1
                elif(float(thisRecord['money'])>11):
                    distribution['11-50'] = distribution['11-50']+1
                else:
                    distribution['lessThan10'] = distribution['lessThan10']+1

        if len(Response['list']) == 15:
            pages += 1
            Data = '{{"ismore":true,"limit":15,"id":"{0}","offset":{2},"requestTime":{1},"pf":"h5"}}'.format(pro_id,
                                                                                                             int(
                                                                                                                 time.time() * 1000),
                                                                                                             pages * 15)
            Response = SendRequest('https://www.tao-ba.club/idols/join', Data)
        else:
            Cleared = True

    return getPhaseTotal(Founderlist, startTime, endTime, 600)


def getPhaseTotal(Founderlist, startTime, endTime, interval):
    phaseRecord = []
    total = 0
    timestamp = startTime

    flag = 0
    startTime = startTime + flag * interval

    for idx, item in enumerate(reversed(Founderlist)):
        total += float(item['money'])

        if (item['stime'] > startTime):
            record = {"timestamp": startTime, "total": str(('%0.2f' % total))}
            phaseRecord.append(record)

            flag += 1
            startTime = startTime + interval

        if (startTime > endTime + 10 and idx == len(Founderlist) - 1):
            record = {"timestamp": endTime, "total": str(('%0.2f' % total))}
            phaseRecord.append(record)

    return phaseRecord
