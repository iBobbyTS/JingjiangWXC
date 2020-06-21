import requests
from lxml import etree

url = 'http://www.jjwxc.net/onebook.php?novelid=3919578'
addChapterIndex = False

res = requests.get(url)
res.encoding = 'gb18030'
res = etree.HTML(res.text)
name = res.xpath('/html/body/table[2]/tbody/tr[1]/td/div/span/h1/span/text()')[0]
file = open(f'{name}.txt', 'a')
info = res.xpath('/html/body/table[2]/tbody/tr')[3:-1]
# info = info[19:20]
content = []
for i in info:
    count = i.xpath('td[1]/text()')[0].replace(' ', '').replace('\n', '').replace('\r', '')
    title = i.xpath('td[2]/span/div[1]/a/text()')
    if title:
        title = title[0]
        main = i.xpath('td[3]/text()')[0].replace('  ', '').replace('\n', '').replace('\r', '')
        url = i.xpath('td[2]/span/div[1]/a/@href')[0]
        res2 = requests.get(url)
        res2.encoding = 'gb18030'
        res2 = etree.HTML(res2.text)
        content1 = res2.xpath('/html/body/table[1]/tr[2]/td[1]/div/text()')
        if addChapterIndex:
            title = f'第{count}章 {title}'
        content2 = [title, main]
        for i2 in content1:
            i2 = i2.replace('  ', '').replace('\n', '').replace('\r', '').replace('\u3000', '')
            if i2:
                content2.append(i2)
        writerWantsToSay = res2.xpath('/html/body/table[1]/tr[2]/td[1]/div/div[@class="readsmall"]/text()')
        writerWantsToSay = '\n'.join(writerWantsToSay)
        content2.append(writerWantsToSay)
        content2 = '\n'.join(content2)
        content.append(content2)
        print(f'已完成 {title}')
content = '\n\n'.join(content)
file.write(content)
file.close()
print('已保存')
