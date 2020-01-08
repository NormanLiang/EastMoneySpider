# -*- coding:utf-8 -*-
import asyncio
from enum import Enum
from lxml import etree
import aiohttp
import json
import csv
import os
import sys


INDEX = 0
INDEX_URL = '{index}'
ALL_STOCK_URL = 'http://58.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112404022616643111314_1577348310244&pn=' + INDEX_URL + '&pz=20&po=0&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f12&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'

URL_LIST = []
XC_HELPER = []
MAX_XIECHENG_NUM = 20
MAX_PAGES = 20

CODE_LIST = []

CODE_URL = '{code}'
STOCK_PRICE_URL = 'http://65.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112409626744256448716_1578291373655&secid=' + CODE_URL + '&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&klt=101&fqt=0&end=20500101&lmt=1000000&_=1578291373803'
STOCK_PRICE_URL_HOUFUQUAN = 'http://18.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery1124024716912013697212_1578364158697&secid=' + CODE_URL + '&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&klt=101&fqt=2&end=20500101&lmt=1000000&_=1578364158841'
STOCK_PRICE_URL_QIANFUQUAN = 'http://6.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery1124024716912013697212_1578364158697&secid=' + CODE_URL + '&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&klt=101&fqt=1&end=20500101&lmt=2360&_=1578364158734'

STOCK_DIR_BU = 'stock'
STOCK_DIR_QIAN = 'stock_qian'
STOCK_DIR_HOU = 'stock_hou'

FUQUAN = 0

HEADER = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cookie':'qgqp_b_id=1822648fc403ecffdc22e3939222bfe3; st_si=49364384037474; st_asi=delete; HAList=a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC; em_hq_fls=js; st_pvi=97203080784168; st_sp=2019-11-14%2014%3A27%3A29; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=16; st_psi=20191227104158448-113200301321-2756835653',
    'referer': 'http://quote.eastmoney.com/center/gridlist.html',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

TITLE_STR = ['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅']

class FU_QUAN_TYPE(Enum):
    BU_FU_QUAN = 0,
    QIAN_FU_QUAN = 1,
    HOU_FU_QUAN = 2,

class URL_TYPE(Enum):
    URL_CODE = 0
    URL_PRICE = 1

class XIECHENG_STATE(Enum):
    STATE_IDLE = 0
    STATE_BUSY = 1

class XIECHENG_Helper():
    
    def __init__(self, id):
        self.id = id
        self.state = XIECHENG_STATE.STATE_IDLE
        self.running = True

    def getID(self):
        return self.id    

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def isBusy(self):
        return True if self.state == XIECHENG_STATE.STATE_BUSY else False

    def setRunning(self, running):
        self.running = running
    
    def getRunning(self):
        return self.running

STOCK_DIRS = {
    FU_QUAN_TYPE.BU_FU_QUAN: STOCK_DIR_BU,
    FU_QUAN_TYPE.QIAN_FU_QUAN: STOCK_DIR_QIAN,
    FU_QUAN_TYPE.HOU_FU_QUAN: STOCK_DIR_HOU,
}

STOCK_URLS = {
    FU_QUAN_TYPE.BU_FU_QUAN: STOCK_PRICE_URL,
    FU_QUAN_TYPE.QIAN_FU_QUAN: STOCK_PRICE_URL_QIANFUQUAN,
    FU_QUAN_TYPE.HOU_FU_QUAN: STOCK_PRICE_URL_HOUFUQUAN,
}

def open_json(tar):
    js = None
    try:
        js = json.loads(tar, encoding='utf-8')
    except Exception as e:
        print(e)
        #click.echo('json open failed')
        pass

    return js

def initial():

    for i in range(0, MAX_PAGES*MAX_XIECHENG_NUM):
        URL_LIST.append(ALL_STOCK_URL.replace(INDEX_URL, str(i+1)))

def getURLFromPool():

    if len(URL_LIST) > 0:
        return URL_LIST.pop(0), URL_TYPE.URL_CODE
    else:
        if len(CODE_LIST) > 0:
            code = CODE_LIST.pop(0)[0]

            stock_url = STOCK_URLS.get(FUQUAN)

            if code.startswith('60'):
                url_ret = stock_url.replace(CODE_URL, '1.'+code)
            else:
                url_ret = stock_url.replace(CODE_URL, '0.'+code)
            return url_ret, URL_TYPE.URL_PRICE

    return None, None

def parseJSON(json_data):

    try:
        edges = json_data['data']['diff']

        for edge in edges:
            code = edge['f12']
            name = edge['f14']
            if code is not None:
                CODE_LIST.append((code, name))

    except Exception as e:
        pass

def parse_code_content(content):
    parseJSON(content)


def parse_price_content(json_data):

    try:
        edges = json_data['data']['klines']
        code = json_data['data']['code']
        name = json_data['data']['name']

        stockdir = STOCK_DIRS.get(FUQUAN)
        with open(stockdir+'/'+code+'.csv', '+w') as f:
            print('writing data of ', code, '...')
            f_csv = csv.writer(f)
            f_csv.writerow(TITLE_STR)
            for edge in edges:
                data = edge.split(',')
                f_csv.writerow(data)

    except Exception as e:
        pass

def parse_data(content, url_type):

    methods = {
        URL_TYPE.URL_CODE: parse_code_content,
        URL_TYPE.URL_PRICE: parse_price_content,
    }

    content = str(content, encoding='utf-8')
    if content.startswith('jQuery'):
        content = content.split('(')[1]
        content = content.split(')')[0]

    js_data = open_json(content)
    method = methods.get(url_type)

    if js_data is not None and method is not None:
        return method(js_data)
    else:
        return None

async def request_and_parse(url, url_type):

    while True:

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=HEADER) as resp:

                        if resp.status == 200:
                            data = await resp.read()
                            parse_data(data, url_type)

        except Exception as e:
            print(e)
            
        break
        
def sendStopSignal():
    
    running = False
    res = False

    for xc in XC_HELPER:
        if xc.isBusy():
            running = True
            break

    if running == False:

        for xc in XC_HELPER:
            xc.setRunning(False)

        res = True
    
    return res
  
async def crawl_url(id):

    while True:

        url, url_type = getURLFromPool() 

        if url is not None:
            XC_HELPER[id].setState(XIECHENG_STATE.STATE_BUSY)
            await request_and_parse(url, url_type)
        else:
            XC_HELPER[id].setState(XIECHENG_STATE.STATE_IDLE)
            await asyncio.sleep(1)

        if id == 0:
            stop = sendStopSignal()

        if XC_HELPER[id].getRunning() == False:
            break

def main():
    stockdir = STOCK_DIRS.get(FUQUAN)

    folder = os.getcwd() + '/' + stockdir
    if not os.path.exists(folder):
        os.makedirs(folder)

    initial()
    tasks = []
    for i in range(0, MAX_XIECHENG_NUM):
        xc = XIECHENG_Helper(i)
        gen = crawl_url(xc.getID())
        tasks.append(gen)
        XC_HELPER.append(xc)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()        

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == '1' or sys.argv[1] == 'Qian' or sys.argv[1] == 'qian':
            FUQUAN = FU_QUAN_TYPE.QIAN_FU_QUAN
        elif sys.argv[1] == '2' or sys.argv[1] == 'Hou' or sys.argv[1] == 'hou':
            FUQUAN = FU_QUAN_TYPE.HOU_FU_QUAN
        else:
            FUQUAN = FU_QUAN_TYPE.BU_FU_QUAN

    else:
        FUQUAN = FU_QUAN_TYPE.BU_FU_QUAN
        
    main()

