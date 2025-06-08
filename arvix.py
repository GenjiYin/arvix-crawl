import re
import os
import time
import requests
from lxml import etree

class paper_crawl:
    def __init__(self, date, proxy='http://127.0.0.1:7890'):
        self.date = date
        self.proxies = {'http': proxy, 'https': proxy}
        self.reference = 'https://arxiv.org'
        self.urls = self.reference + f'/catchup/q-fin/{date}?abs=False'

        # 新建一个文件夹
        self.folder_path = os.path.join(os.getcwd(), 'assets')
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    def _download(self, url, title, path):
        title = re.sub(r'[^\w\s]', '', title)
        path = os.path.join(path, f'{title}.pdf')
        if os.path.exists(path):
            print(f'论文: {title} 已存在')
            return
        f = open(path, mode='wb')
        f.write(requests.get(url, proxies=self.proxies).content)
        f.close()
        print(f'论文: {title} 下载完毕')
    
    def daily_run(self):
        r = requests.get(self.urls, proxies=self.proxies)
        html = etree.HTML(r.text)
        if len(html.xpath('//main/div/div/div/dl/dd')) == 0:
            print('当天无论文')
            return
        for title, pdf in zip(html.xpath('//main/div/div/div/dl/dd'), html.xpath('//main/div/div/div/dl/dt')):
            # 获取论文标题
            t = title.xpath('div/div[@class="list-title mathjax"]/text()')[0].replace('\n', '')
            t = ' '.join(list(filter(lambda x: x.strip(), t.split(' '))))

            # 获取论文链接
            p = pdf.xpath('a[@title="Download PDF"]/@href')[0]
            p = 'https://arxiv.org' + p

            # 保存文件的地址
            save_path = os.path.join(self.folder_path, self.date)
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            self._download(p, title=t, path=save_path)
            time.sleep(1.5)

if __name__ == '__main__':
    p = paper_crawl('2025-06-04')
    p.daily_run()