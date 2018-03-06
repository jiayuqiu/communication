# coding:utf-8

'''
获取数字货币的历史价格
'''

print(__doc__)

# --------------------------
import urllib
import urllib.request
import time
import lxml
import re
import pandas as pd

from bs4 import BeautifulSoup
from lxml.html import tostring

# --------------------------------------------------------------
# xpath爬取网页数据，中文解码
def _callback(matches):
    id = matches.group(1)
    try:
        return chr(int(id))
    except:
        return id


def decode_unicode_references(data):
    return re.sub("&#(\d+)(;|(?=\s))", _callback, str(data))
# ---------------------------------------------------------------

def timestamp2timestr(timestamp):
    '''
    时间戳格式转换年月日
    :param timestamp: 时间戳
    :return: 年月日
    '''
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y%m%d", timeArray)
    return otherStyleTime

# ----------------------------------------------------------------
def crawler_func(url):
    '''
    爬虫程序段
    :return:
    '''
    # bitcoin_url = 'https://coinmarketcap.com/zh/currencies/ethereum/historical-data/?start=20130225&end=20180305'
    print(url, '\n')
    # bitcoin_url = "http://www.smb.gov.cn/sh/tqyb/qxbg/index.html"
    headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
               'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
               'Connection': 'keep-alive'}
    
    req = urllib.request.Request(url, headers=headers)
    page_source = urllib.request.urlopen(req).read().decode()
    bs_page_source = BeautifulSoup(page_source, "html.parser").decode()
    root_page = lxml.etree.HTML(bs_page_source)
    
    # 获取表头
    tb_thead_xpath = '//*[@id="historical-data"]/div/div[3]/table/thead'
    root_tb_thead_list = root_page.xpath(tb_thead_xpath)
    tb_thead_string = decode_unicode_references(tostring(root_tb_thead_list[0]))
    col_name_pattern = re.compile(u'<th class=.*?>(.*?)</th>', re.S)
    col_name_list = re.findall(col_name_pattern, tb_thead_string)
    # ['日期', '开盘价', '最高价', '最低价', '收盘价', '交易量', '市值']
    
    # 获取表内数据
    tb_body_xpath = '//*[@id="historical-data"]/div/div[3]/table/tbody'
    root_tb_body_list = root_page.xpath(tb_body_xpath)
    tb_body_string = decode_unicode_references(tostring(root_tb_body_list[0]))
    # print(tb_body_string)
    
    # 日期
    tb_date_pattern = re.compile(r'<td class=.*?>(.*?)</td>', re.S)
    tb_date_list = re.findall(tb_date_pattern, tb_body_string)
    
    # 开盘价、最高价、最低价、收盘价
    tb_ohlc_pattern = re.compile(r'<td data-format-fiat="" data-format-value=.*?>(.*?)</td>', re.S)
    tb_ohlc_list = re.findall(tb_ohlc_pattern, tb_body_string)
    
    # 转换开盘价、最高价、最低价、收盘价的格式
    open_price_list = list()
    high_price_list = list()
    low_price_list = list()
    close_price_list = list()
    for index in range(0, len(tb_ohlc_list)):
        if index % 4 == 0:
            # 当天开盘价
            open_price = tb_ohlc_list[index]
            open_price_list.append(open_price)
        elif index % 4 == 1:
            # 当天最高价
            high_price = tb_ohlc_list[index]
            high_price_list.append(high_price)
        elif index % 4 == 2:
            # 当天最低价
            low_price = tb_ohlc_list[index]
            low_price_list.append(low_price)
        elif index % 4 == 3:
            # 当天收盘价
            close_price = tb_ohlc_list[index]
            # print('close_price = %s' % close_price)
            close_price_list.append(close_price)
    
    # 交易量、市值
    tb_market_data_pattern = re.compile(r'<td data-format-market-cap="" data-format-value=.*?>(.*?)</td>')
    tb_market_data_list = re.findall(tb_market_data_pattern, tb_body_string)
    
    # 转换交易量、市值格式
    trading_value_list = list()
    market_value_list = list()
    for index in range(0, len(tb_market_data_list)):
        if index % 2 == 0:
            # 交易量
            trading_value = tb_market_data_list[index]
            trading_value_list.append(trading_value)
        elif index % 2 == 1:
            # 当天最高价
            market_value = tb_market_data_list[index]
            market_value_list.append(market_value)
    
    coin_history_df = pd.DataFrame(columns=col_name_list)
    coin_history_df[u'日期'] = tb_date_list
    coin_history_df[u'开盘价'] = open_price_list
    coin_history_df[u'最高价'] = high_price_list
    coin_history_df[u'最低价'] = low_price_list
    coin_history_df[u'收盘价'] = close_price_list
    coin_history_df[u'交易量'] = trading_value_list
    coin_history_df[u'市值'] = market_value_list
    coin_history_df.to_csv('以太坊历史价格.csv', index=None)
    

if __name__ == '__main__':
    url = 'https://coinmarketcap.com/zh/currencies/ethereum/historical-data/?start=20130225&end=20180305'
    crawler_func(url)
    print('done!')
