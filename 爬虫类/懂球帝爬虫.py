# 这个程序提供了访问懂球帝网页版的方式，仅供参考
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


TITLE = '懂球帝赞数统计表'  # 表格名称
START_NUM = 1307230  # 第一个需要爬取的页面序号
END_NUM = 1307289  # 最后一个需要爬取的页面序号


wb = Workbook()
sheet = wb.active
sheet.title = TITLE
commentcontent = []


def get_html(url):
    text = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'})
    text.encoding = text.apparent_encoding
    return text.text


def zannum(text):
    soup = BeautifulSoup(text, 'html.parser')
    commenttaglist = soup.find_all('div', class_='comment-con')
    taglist = soup.find_all('span', class_='comment-num')
    commentlist = []
    for i in range(len(taglist)):
        comment=str(commenttaglist[i])[28:-19]
        commentcontent.append(comment)
        commentlist.append(str(taglist[i]))
        zannum=int(str(commentlist[i])[26:-7])
        yield zannum

        
def content():
    for i in range(len(commentcontent)):
        content = commentcontent[i]
        print(content)
        yield str(content)


def get_url(m,n):
    for i in range(m,n+1,2):
        tem = "http://www.dongqiudi.com/news/"+str(i)+'.html'
        yield tem


def get_num(m,n):
    zanlist = []
    contentlist = []
    for i in get_url(m, n):
        for j in zannum(get_html(i)):
            zanlist.append(j)
    for j in content():
        contentlist.append(j)
    for i in range(len(zanlist)):
        sheet['A%d' % (i+1)] = str(contentlist[i])
        sheet['B%d' % (i+1)].value = zanlist[i]
    wb.save(TITLE + '.xlsx')

            
if __name__=='__main__':
    get_num(START_NUM, END_NUM)
