import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import re
import time
import codecs
from pathlib import Path
from tqdm import tqdm


WC_MASK_IMG = 'wordcloudtem.png'
WC_FONT_PATH = 'msyh.ttc'
UA = UserAgent()
SHOP_DICT = {
    '肥肥虾庄': 'H3MIAIJ0pvC9COjH',
    '虾皇': 'H4gteEXB0MeizRtP',
    '巴厘龙虾': 'k2BSrkYa72yPncno',
    '靓靓蒸虾': 'k6CzLcEzlMxIB852',
    '一棠龙虾': 'EiGJm5ZBMpTO7F4G',
    '江城肥仔虾庄': 'iIofJNXTyKfN8lCj',
    '阿木龙虾': 'i6ox46l0JYLOuFm1',
    '皮皮大排档': 'l6TFiY6OSdaK7gb1'
}
COOKIES = [
    "_lxsdk_cuid=173cd396b42c8-000da41105b3da-3323765-1fa400-173cd396b42c8; " +
    "_lxsdk=173cd396b42c8-000da41105b3da-3323765-1fa400-173cd396b42c8; " +
    "Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1596875959; " +
    "_hc.v=ddbbaeab-4a5e-c368-0eb0-1e629f20a297.1596875960; fspop=test; " +
    "dplet=14a134af5461d0e6d8d22f712ac1d298; " +
    "dper" +
    "=fa392156e11d5d196027e3d53d85bafeb4a9616c7773e51ba03331fe6ea1cddb7f490d629ae32f16c826cd" +
    "b4a235fcbf19ddedbf719c5db9000eb08ca7396aae0e85297501de6db5ba"
    "d3b53502ff52d58e668621d30493526f4ceddeb5be2b1d; " +
    "ll=7fd06e815b796be3df069dec7836c3df; " +
    "ua=%E5%86%AF%E6%97%B6; " +
    "ctu=15319da7adfce94ddd57aba336ca489399f83bdf457a497cacd3c339060a6bd7; " +
    "s_ViewType=10; aburl=1; cy=70; cye=changchun; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1596889455; " +
    "_lxsdk_s=173ce06317d-330-5c9-a61%7C%7C132",
    "_lxsdk_cuid=171c55eb43ac8-07f006bde8dc41-5313f6f-1fa400-171c55eb43ac8; " +
    "_lxsdk=171c55eb43ac8-07f006bde8dc41-5313f6f-1fa400-171c55eb43ac8; " +
    "_hc.v=970ed851-cbab-8871-10cf-06251d4e64a0.1588154251; " +
    "t_lxid=17186f9fa02c8-02b79fa94db2c8-5313f6f-1fa400-17186f9fa03c8-tid; " +
    "_lxsdk_s=171c55ea204-971-8a9-eae%7C%7C368"
]


def header_generator():
    header = {'User-Agent': UA.random}
    cookie = random.choice(COOKIES)
    header['Cookie'] = cookie
    return header


def get_remark_num(num):
    url = 'http://www.dianping.com/shop/' + str(num) + '/review_all/p1'
    r = requests.get(url, headers=header_generator())
    soup = BeautifulSoup(r.text, 'html.parser')
    print('--------Finding the Number of Pages--------')
    label_list = soup.find_all('a', class_='PageLink')
    print(int(str(label_list[-1])[-6:-4]))
    return int(str(label_list[-1])[-6:-4])


def get_text(num, page_num):
    url = 'http://www.dianping.com/shop/' + str(num) + '/review_all/p' + str(page_num)
    r = requests.get(url, headers=header_generator())
    soup = BeautifulSoup(r.text, 'html.parser')
    # print('--------Crawling Page ' + str(page_num) + '--------')
    label_list = soup.find_all('div', class_='review-words Hide')
    remark_list = []
    for count, content in enumerate(label_list):
        # print('--------Page ' + str(page_num) + ' Remark ' + str(count+1) + '--------')
        content = re.sub(r'\n', '', str(content.contents))
        content = re.sub(r"</?(.+?)>/?(.+?)</?(.+?)>", '', content)
        content = re.sub(r'(\[\')|(</?(.+?)>)|(\\n)', '', content)
        content = re.sub(r'(\', , \'\'])', '', content).strip()
        # print(content)
        remark_list.append(content)
    return remark_list


def save_text(num, name):
    f = codecs.open(str(name) + ".txt", 'w+', encoding='utf-8')
    page_num = get_remark_num(num)
    page_list = list(range(page_num))
    for page in page_list:
        page_list[page] = page + 1
    random.shuffle(page_list)
    for page in tqdm(page_list):
        try:
            remark_list = get_text(num, page)
            tmp = 0
            while not remark_list:
                # print('-------- Retrying Crawl--------')
                time.sleep(random.randint(10, 20))
                remark_list = get_text(num, page)
                tmp += 1
                if tmp >= 10:
                    break
        except:
            print('There is an error!')
            continue
        else:
            for remark in remark_list:
                f.write(remark + '\n')
        time.sleep(random.randint(10, 20))
    f.close()


def cut_word(path):
    with open(path, encoding='utf-8') as file:
        comment_txt = file.read()
        wordlist = jieba.cut(comment_txt, cut_all=True)
        wl = " ".join(wordlist)
        # print(wl)
        return wl


def create_word_cloud(num, name):
    wc_mask = np.array(Image.open(WC_MASK_IMG))
    wc = WordCloud(background_color="white", max_words=2000, mask=wc_mask, scale=4,
                   max_font_size=50, random_state=42, font_path=WC_FONT_PATH)
    path = str(name) + '.txt'
    if Path(path).exists():
        pass
    else:
        save_text(num, name)
    wc.generate(cut_word(path))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(str(name) + '.png', dpi=300)
    plt.figure()
    # plt.show()


if __name__ == '__main__':
    for name, num in SHOP_DICT.items():
        if Path(str(name) + '.png').exists():
            continue
        else:
            print('--------' + 'Crawling ' + str(name) + '--------')
            create_word_cloud(num, name)
            time.sleep(random.randint(15, 30))
