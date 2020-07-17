# python爬虫
import requests
import json
from bs4 import BeautifulSoup

import os

from time import sleep
# 写入excel
import xlwt
# 读取excel
import xlrd
# 修改excel
from xlutils.copy import copy

# 自动化工具 模拟浏览器行为
from selenium import webdriver
from selenium.webdriver import ActionChains

def  getJuejinListByRequest():
    # 获取掘金列表
    # 首页地址
    url = "https://web-api.juejin.im/query"
    # 伪装成浏览器
    headers = {
        'Origin': 'https://juejin.im',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'X-Legacy-Token': 'eyJhY2Nlc3NfdG9rZW4iOiJBNVNuRUNPb1Jad0doWm1wIiwicmVmcmVzaF90b2tlbiI6IkpuVkFoZFozdjNFdDZMOFMiLCJ0b2tlbl90eXBlIjoibWFjIiwiZXhwaXJlX2luIjoyNTkyMDAwfQ==',
        'Content-Type': 'application/json',
        'Referer': 'https://juejin.im/user/5c3f3c415188252b7d0ea40c',
        'X-Legacy-Uid': '5dd631975188254e310b4cbb',
        'X-Agent': 'Juejin/Web',
        'Set-Cookie': 'QINGCLOUDELB=743155a837e7deb03acb8e760501fb609b6845ac24ccb3b2c31a11c11a0765c2|Xvm5A|Xvm5A; path=/; HttpOnly',
        'X-Request-Id': 'ba2731e0b9ed11eab6b66f8b0073adbf'
    }

    payload = '{"operationName":"","query":"","variables":{"first":"20","after":"","order":"POPULAR"},"extensions":{"query": {"id":"21207e9ddb1de777adeaca7a2fb38030"}}}'

    # 发起网络请求，获取到返回的html
    result = requests.post(url=url, headers=headers, data=payload).content.decode('utf-8')
    #  json.loads()用于将str类型的数据转成dict。
    result=json.loads(result) 
    result_list=result['data']['articleFeed']['items']['edges']

    # excel
    workbook = xlwt.Workbook(encoding = 'ascii')
    worksheet = workbook.add_sheet('MyWorksheet')
    # 参数对应 行, 列, 值
    worksheet.write(0, 0, '标题') 
    worksheet.write(0, 1, '用户名') 


    for index in range(len(result_list)):
        print(index)
        title = result_list[index]['node']['title']
        username = result_list[index]['node']['user']['username']
        print(title)
        print(username)

        worksheet.write(index+1, 0, title) 
        worksheet.write(index+1, 1, username) 


    workbook.save('test.xls') # 保存文件 



def getJuejinListBySelenium():
    
    # 是否存在文件， 有跳过 ， 没有就生成文件
    if(not os.path.exists('boss.xls')):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Selenium')
        # 参数对应 行, 列, 值
        worksheet.write(0,0,'职位')
        worksheet.write(0,1,'公司')
        workbook.save('boss.xls')

    url = "https://www.zhipin.com/c101210100-p100901/?page=1&ka=page-1"


    #声明浏览器
    browser = webdriver.Chrome() 
    browser.get(url)#打开浏览器预设网址
    next_btn = browser.find_element_by_class_name('next')
    classStr = next_btn.get_attribute('class')

    # 打开excel文件
    data = xlrd.open_workbook('boss.xls')
    # 获取excel表名为Selenium的表
    table = data.sheet_by_name('Selenium') 
    # 获取 表的行数
    nrows = table.nrows 
    new_workbook = copy(data)
    new_worksheet = new_workbook.get_sheet(0)

    while (classStr.find('disabled') == -1):
        next_btn.click()
        sleep(3)
        next_btn = browser.find_element_by_class_name('next')
        classStr = next_btn.get_attribute('class')
        jobsList = browser.find_elements_by_css_selector('.job-primary')
        for item in jobsList:
            jobName_text = item.find_elements_by_css_selector('.job-name a')[0].text
            company_text = item.find_elements_by_css_selector('.company-text .name a')[0].text

            new_worksheet.write(nrows ,0, jobName_text)
            new_worksheet.write(nrows ,1, company_text)
            nrows = nrows+1

        new_workbook.save('boss.xls')
    
    browser.quit()



getJuejinListBySelenium()


