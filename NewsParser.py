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
        for i in range(len(urls)):
                    u = urls[i]
                    d = data[i]
                    if (fuzz.partial_ratio(data[i], corona) > 80) or (fuzz.partial_ratio(data[i], covid) > 80):
                        pack.append(
                            {
                                'title': d,
                                'url': str(u)
                            }
                        )
        return(pack)

    def riaParser(self):
        url = 'https://ria.ru/'
        r = requests.get(url)
        if r.ok: # 200  ## 403 404
            html = r.text
        soup = BeautifulSoup(html, 'lxml')
        title = "aaa"
        title =soup.find_all('span',{'class':'cell-list__item-title'})
        link_containers=soup.findAll('div',{'class':'cell-list__item m-no-image'})
        data = []

        for text in title:
            if text.text != ' ':
                data.append(text.text)
        counter = 0
        urls = []
        for i in range(3):
            a_tag = link_containers[i] .find("a")
            # Если нашел
            if a_tag:
                link = a_tag.get("href")
                if link != "?rcmd_alg=slotter":
                    urls.append(urljoin(url, link))
            else:
                counter += 1
        print(f"Ошибок нашлось {counter}")
        return self.findCorona(urls, data)

def main():
    parser = NewsParser()
    print(parser.riaParser())


if __name__ == '__main__':
    main()