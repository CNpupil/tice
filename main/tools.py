import hashlib
import time
import re
import random
import string
import base64
from Crypto.Cipher import AES
from django.core.paginator import Paginator
from datetime import datetime, timedelta
import geoip2.database
import datetime


# 验证类，通过addCheck()增加验证规则，start()进行统一验证
# 验证类的check开头的方法，如果验证通过为True，否则为False
class Validate:
    def __init__(self):
        self.funList = []
        self.dataList = []
        self.msgList = []
        self.checkValueList = []

    def clear(self):
        self.funList.clear()
        self.dataList.clear()
        self.msgList.clear()
        self.checkValueList.clear()

    def startCheck(self):
        ok = True
        for i in range(len(self.funList)):
            if self.checkValueList[i] is None or self.checkValueList[i] == '':
                ok = ok and getattr(self, self.funList[i], None)(self.dataList[i])
            else:
                ok = ok and getattr(self, self.funList[i], None)(self.dataList[i], self.checkValueList[i])
            if not ok:
                msg = self.msgList[i]
                self.clear()
                return False, msg
        self.clear()
        return True, 'ok'

    def addCheck(self, fun, data, msg, checkValue=''):
        if not hasattr(self, fun):
            return False
        self.funList.append(fun)
        self.dataList.append(data)
        self.msgList.append(msg)
        self.checkValueList.append(checkValue)
        return True

    def checkIsNotEmpty(self, data, *args):
        if data is None or len(str(data)) <= 0:
            return False
        return True

    def checkMaxLength(self, data, length=20):
        data = str(data)
        return len(data) <= length

    def checkMinLength(self, data, length=0):
        data = str(data)
        return len(data) >= length

    def checkMinValue(self, data, minValue=0):
        data = int(data)
        return data >= minValue
    
    def checkMaxValue(self, data, maxValue=0):
        data = int(data)
        return data <= maxValue

    def checkIsEmail(self, data, *args):
        return re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", data) != None

    def checkHasNoSpace(self, data, *args):
        return str(data).find(' ') == -1 and str(data).find('\t') == -1

    def checkOnlyNumal(self, data):
        return data.isalnum()
    
    def checkIsDomain(self, data):
        pattern = re.compile(
            r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA -Z0-9]))\.'
            r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
        )
        return True if pattern.match(data) else False
    
    def checkIsNumber(self, data):
        return str(data).isdigit()
    
    def checkIsNotNagetiveNumber(self, data):
        return int(data) >= 0

# Validate使用过程
# ck = Validate()
# data = 30
# ck.addCheck('empty', data, 'null')
# ck.addCheck('maxLength', data, 'maxlength')
# print(ck.start())

class AesOp:
    def __init__(self):
        self.password = b'1234567812345678' #秘钥，b就是表示为bytes类型
        self.iv = b'1234567812345678' # iv偏移量，bytes类型

    def addTo32(self, text):
        if len(text) < 32:
            text = text + ((32 - len(text)) * '=')
        return text

    def aesEncode(self, text):
        aes = AES.new(self.password, AES.MODE_CBC, self.iv)
        return aes.encrypt(text) 

    def aesDecode(self, text):
        aes = AES.new(self.password, AES.MODE_CBC, self.iv) #CBC模式下解密需要重新创建一个aes对象
        return str(aes.decrypt(text), 'utf-8').replace('=', '')
    


def genearteMD5(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()

def getNowTimeStamp():
    return int(time.time())

def getTimeStr(timeStamp):
    return datetime.datetime.fromtimestamp(timeStamp)

def generateString16():
    # random.sample('1234567890abcdefghijklmnopqrstuvwxyz!@#$%^&*()', 16)
    randStr = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    return randStr

def generateString32():
    randStr = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    return randStr

def generateCode6():
    randStr = ''.join(random.sample(string.digits, 6))
    return randStr

def b64Encode(data):
    b64Code = base64.b64encode(str(data).encode())
    return b64Code

def b64Decode(data):
    data = base64.b64decode(str(data)).decode()
    return data

def myPaginator(data, maxSize, pageNum=1):
    paginator = Paginator(data, maxSize)
    pageNum = int(pageNum)
    pageCount = paginator.num_pages
    if pageNum > pageCount:
        data = {}
    else:
        data = paginator.page(int(pageNum))
    return data, pageCount

def getTodayBeginTimeStamp(nowTime):
    return nowTime - (nowTime- time.timezone)%86400

def isSameDay(timestamp1, timestamp2):
    # d1 = datetime.fromtimestamp(timestamp1)
    # d2 = datetime.fromtimestamp(timestamp2)
    # return (d1.date() == d2.date() and
    #         abs(d1 - d2) <= timedelta(hours=24))
    return getTodayBeginTimeStamp(timestamp1) == getTodayBeginTimeStamp(timestamp2)

def getIp(request):
    '''获取请求者的IP信息'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip