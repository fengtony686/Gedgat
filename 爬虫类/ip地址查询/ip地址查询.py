import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time


SLEEP_TIME = 60  # IP检测间隔时间为60秒 
CHART_NAME = r'ip地址统计表'  # 表格的名称
NUMBER_OF_IP = 50  # 获取IP的数量 


wb = Workbook()
sheet = wb.active
sheet.title = CHART_NAME


def get_html(url):
    text = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'})
    text.encoding = text.apparent_encoding
    return text.text


def ip(text):
    soup = BeautifulSoup(text, 'html.parser')
    ip_address = soup.find_all('strong', class_='your-ip')
    ip=str(ip_address[0])[57:-9]
    return ip

    
def address(ip):
     r = requests.get('http://ip.taobao.com/service/getIpInfo.php?ip=%s' %ip)  # 阿里的IP归属地查询接口
     if  r.json()['code'] == 0 :
         i = r.json()['data']
         country = i['country']  #国家 
         area = i['area']        #区域
         region = i['region']    #地区
         city = i['city']        #城市
         isp = i['isp']
         print(country)
         return country,area,region,city,isp
     else:
         print('Error!')


def get_ip(num):
    url='https://whoer.net/zh'  # 一个可以检测到代理IP的网站
    for i in range(num):
        try:
            text = get_html(url)
            sheet['A%d' % (i+1)] = ip(text)
            sheet['B%d' % (i+1)] = address(ip(text))[0]
            sheet['C%d' % (i+1)] = address(ip(text))[1]
            sheet['D%d' % (i+1)] = address(ip(text))[2]
            sheet['E%d' % (i+1)] = address(ip(text))[3]
            sheet['f%d' % (i+1)] = address(ip(text))[4]
            time.sleep(SLEEP_TIME)
        except:
            time.sleep(SLEEP_TIME)
            continue
    wb.save(CHART_NAME + '.xlsx')


if __name__ == '__main__':
    get_ip(NUMBER_OF_IP)
