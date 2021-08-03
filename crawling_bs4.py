from urls import *
import requests
from bs4 import BeautifulSoup

import os
import datetime
import django
from send_notification import send_message
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from postbox.models import Notice, Keyword


def crawling_bypage(url, page):
    url = url + '?page=' + str(page)
    req = requests.get(url)
    # html 소스 가져오기
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    tbody = soup.find('tbody')
    trs = tbody.findAll('tr')

    # 전체 공지사항 갯수 구하기
    total_trs = len(trs)

    # 고정된 공지사항 갯수 구하기
    headline_trs = soup.findAll('tr', 'headline')
    fixedNum = len(headline_trs)

    data = {}
    # 고정된 공지사항을 제외한 공지
    trs_mn = trs[fixedNum:total_trs]
    for tr in trs_mn:
        notices = []
        title_list = {}
        basic_url = 'https://www.sungshin.ac.kr'
        a = tr.find('a')
        # 공지사항 제목
        title = a.find('strong').text.strip()
        # 공지사항 url
        url = basic_url + tr.find('a')['href']
        # 공지사항 날짜
        day = tr.findAll('td')[2].text.strip()
        date = datetime.datetime.strptime(day, '%Y.%m.%d')

        notices.append(url)
        notices.append(date)
        data[title] = notices

    return data


data = {}


def crawling(url, page):
    for i in range(1, page + 1):
        print(url)
        data.update(crawling_bypage(url, i))


# 학사공지
crawling(hacksa, 2)
# 일반공지
crawling(normal, 2)
# 입학공지
crawling(admission, 2)
# 취업공지
crawling(employment, 2)
# 대학원(외국인)공지
crawling(graduated_foreigner, 2)

# 컴퓨터공학과
crawling(computer, 2)
crawling(computer_hire, 2)
#
# 청정융합에너지공학과
crawling(cleanEnergy_hire, 1)
crawling(cleanEnergy_outdoor, 1)

# 바이오생명공학과
crawling(biotechnology, 2)
crawling(biotechnology_hire, 1)

# 바이오식품공학과
crawling(biofood_notice, 2)

# 융합보안공학과
crawling(security, 2)
crawling(security_hire, 2)

# 정보시스템공학과
crawling(informationSystems, 2)

# 서비스디자인공학과
crawling(serviceDesign, 2)
crawling(serviceDesign_hire, 1)
crawling(serviceDesign_outoor, 1)

# AI융합학부
crawling(ai, 1)
crawling(ai_outdoor, 1)

# 국어국문학과
crawling(korean, 2)
crawling(korean_outdoor, 2)
crawling(korean_hire, 2)

# 영어영문학과
crawling(english, 2)
crawling(english_outdoor, 1)
crawling(english_hire, 2)

# 독일어문/문화학과
crawling(german_outdoor, 1)
crawling(german_hire, 2)

# 프랑프어문/문화학과
crawling(french, 1)
crawling(french_outdoor, 1)
crawling(french_hire, 2)

# 일본어문/문화학과
crawling(japanese_outdoor, 2)
crawling(japanese_hire, 2)

# 중국어문/문화학과)
crawling(chinese_outdoor, 1)
crawling(chinese_hire, 2)

# 사학과
crawling(history_outdoor, 1)
crawling(history_hire, 2)

# 교육학과
crawling(education_hire, 2)

# 사회교육과
crawling(socialEdu_hire, 2)

# 윤리교육과
crawling(EthicsEdu_hire, 2)

# 한문교육과
crawling(chineseEdu_hire, 2)

# 유아교육과
crawling(childhoodEdu_hire, 2)

# 작곡과
crawling(composition, 2)

# 수학과
crawling(math_hire, 2)

# 통계학과
crawling(statistics_hire, 2)

# it학부
crawling(it_hire, 2)

# 수리통계데이터사이언스학부
crawling(dataScience_outdoor, 1)

# 뷰티산업학과
crawling(beauty, 2)
crawling(beauty_hire, 1)

# 문화예술경영학과
crawling(cultureArt, 2)

# 현대실용음악학과
crawling(music, 2)

# 무용예술학과
crawling(danceArt, 2)

print(data)

for title, notice in data.items():
    notices, created = Notice.objects.get_or_create(title=title, url=notice[0], date=notice[1])

    keywords = Keyword.objects.all()
    if created:
        for keyword in keywords:
            if keyword.keyword in title:
                send_message(title, keyword.keyword)
        notices.save()