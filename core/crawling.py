import requests as req
from bs4 import BeautifulSoup as bfs

def naver_crawling():
    url = 'http://comic.naver.com/webtoon/weekday.nhn'
    headers = {
        'referer': url
    }

    html = req.get(url, headers=headers).text
    soup = bfs(html, 'html.parser')
    up_comic_list = []
    for tag in soup.select('#container #content div.thumb a'):
        if tag.select('em.ico_updt'):
            img_url = tag['href']
            img_tag = tag.find('img')
            title = img_tag['title']

            up_comic_list.append({
                'title': title,
                'img_url': img_url
            })

    return str(up_comic_list)
