import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fuzzywuzzy import fuzz

class NewsParser:
    
    def __init__(self):
        pass
    
    def findCorona(self, urls, data):
        pack = []
        corona = "коронавирус"
        covid = "COVID-19"
        virus = "вирус"
        for i in range(len(urls)):
            u = urls[i]
            d = data[i]
            if (fuzz.partial_ratio(data[i], corona) > 80) or (fuzz.partial_ratio(data[i], covid) > 80) or (fuzz.partial_ratio(data[i], virus) > 80):
                pack.append(
                    {
                        'title': d,
                        'url': str(u)
                    }
                )
            if len(pack) == 3:
                break
        return(pack)

    def getHtml(self, url):
        r = requests.get(url)
        if r.ok: # 200  ## 403 404
            return r.text

    def riaParser(self):
        url = 'https://ria.ru/'
        html = self.getHtml(url)
        soup = BeautifulSoup(html, 'lxml')
        title =soup.find_all('span',{'class':'cell-list__item-title'})
        link_containers=soup.findAll('div',{'class':'cell-list__item m-no-image'})
        data = []
        for text in title:
            if text.text != ' ':
                data.append(text.text)
        counter = 0
        urls = []
        for i in range(3):
            a_tag = link_containers[i].find("a")
            # Если нашел
            if a_tag:
                link = a_tag.get("href")
                if link != "?rcmd_alg=slotter":
                    urls.append(urljoin(url, link))
            else:
                counter += 1
        return self.findCorona(urls, data)
        

    def mailruParser(self):
        url = 'https://news.mail.ru/story/incident/coronavirus/'
        html = self.getHtml(url)
        soup = BeautifulSoup(html, 'lxml')
        title =soup.findAll('span',{'class':'newsitem__title-inner'})
        link_containers=soup.findAll('a',{'class':'newsitem__title link-holder'})
        #print(title)
        data = []
        for text in title:
            if text.text != ' ':
                data.append(text.text)
        counter = 0
        urls = []
        for i in range(10):
            link = link_containers[i].get("href")
            if link != "?rcmd_alg=slotter":
                urls.append(urljoin(url, link))
            else:
                counter += 1
        return self.findCorona(urls, data)

def main():
    parser = NewsParser()
    print(parser.mailruParser())


if __name__ == '__main__':
    main()