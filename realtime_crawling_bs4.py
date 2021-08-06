import time
from datetime import datetime
from url_list import *
import requests
from bs4 import BeautifulSoup


import os
import django
from send_notification import send_message
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from postbox.models import Notice, Keyword


def realtime_crawling(url):
        req = requests.get(url)
        # html 소스 가져오기
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        tbody = soup.find('tbody')
        trs = tbody.findAll('tr')

        # 고정된 공지사항 갯수 구하기
        headline_trs = soup.findAll('tr', 'headline')
        fixedNum = len(headline_trs)

        # 고정된 공지사항을 제외한 최신 공지 5개
        data = {}
        trs_5 = trs[fixedNum:fixedNum + 5]
        for tr in trs_5:
            notices = []
            basic_url = 'https://www.sungshin.ac.kr'
            a = tr.find('a')
            # 공지사항 제목
            title = a.find('strong').text.strip()
            # 공지사항 url
            href = basic_url + tr.find('a')['href']
            # 공지사항 날짜
            day = tr.findAll('td')[2].text.strip()
            date = datetime.strptime(day, "%Y.%m.%d")

            notices.append(href)
            notices.append(date)
            data[title] = notices

        return data


data = {}


def entire_realtime_crawling():
    for url in url_list:
        print(url)
        data.update(realtime_crawling(url))


# 1시간마다 실행행
if __name__ == '__main__':
    while True:
        try:
            entire_realtime_crawling()
        except Exception:
            continue
        break
    print(data)

    for title, notice in data.items():
        notices, created = Notice.objects.get_or_create(title=title, url=notice[0], date=notice[1])

        keywords = Keyword.objects.all()
        if created:
            for keyword in keywords:
                if keyword.keyword in title:
                    send_message(title, keyword.keyword)
            notices.save()

    send_message("1시간마다 실행되나 확인", "test")
