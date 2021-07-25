from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from postbox.models import Notice

# 드라이버 가져오기
desktop_driver = 'C:/Users/user/Downloads/chromedriver_win32/chromedriver.exe'
laptop_driver = 'C:/Users/dldms/Downloads/chromedriver_win32/chromedriver.exe'

driver = webdriver.Chrome(laptop_driver)

# 성신 로그인 페이지에 접속
driver.get('https://portal.sungshin.ac.kr/sso/login.jsp')

def login(id, password):
    sleep(0.5)
    # 포탈 아이디
    driver.find_element_by_name('loginId_mobile').send_keys(id)
    sleep(0.5)
    # 포탈 비밀번호
    driver.find_element_by_name('loginPwd_mobile').send_keys(password)
    # 로그인 버튼 누르기
    driver.find_element_by_xpath('//*[@id="login_mobile"]/div[1]/div/ul/li/ul/div/fieldset/a').click()

# 로그인 수행
login('20190996', 'a!05250525')

def content(url):
    tbody = driver.find_element_by_tag_name("tbody")
    trs = tbody.find_elements_by_tag_name("tr")

    # 작성일
    dateCreated = trs[0].find_element_by_tag_name('td').text.strip()
    dateCreated2 = datetime.datetime.strptime(dateCreated, '%Y.%m.%d')
    writer_ = trs[0].find_elements_by_tag_name('td')
    # 공지 부서
    writer = writer_[1].find_element_by_tag_name('span').text.strip()
    # 제목
    title = trs[1].find_element_by_tag_name('td').text.strip()

    print(dateCreated)
    print(writer)
    print(title)

    # 공지사항 본문
    notice = driver.find_element_by_xpath("//div[@class='viewTxt']").text
    print(notice)

    return title, notice, dateCreated2

def crawling_url_bypage(page, n):
    pageIndex = driver.find_element_by_id('pageIndex')
    nexts = pageIndex.find_elements_by_tag_name('a')
    # 페이지 이동
    nexts[page + 1].click()

    tbody = driver.find_element_by_tag_name('tbody')
    trs = tbody.find_elements_by_tag_name('tr')
    trs_10 = trs[0:10]
    url_list = []
    for tr in trs_10:
        a = tr.find_element_by_class_name('L > div > a')
        source = a.get_attribute('onclick')[34:48]
        # 공지사항 url
        notice_url = 'https://portal.sungshin.ac.kr/board/board.brd?bltnNo=' + source + '&boardId=ssuboard' + n + '&'
        url_list.append(notice_url)

    i = 1
    data = {}
    for url in url_list:
        driver.get(url)
        title, notice, date_created = content(url)
        data[title] = [notice, date_created]
        i = i + 1

    return data

# 학부 학사
def hacksa():
    hacksa_dict = {}

    print("학부학사-----------------------------------------------------------------------------------------------------")
    # 10페이지까지 크롤링
    for i in range(1, 3):
        driver.get('https://portal.sungshin.ac.kr/portal/ssu/menu/notice/ssuboard02.page')
        driver.switch_to.frame('IframePortlet_8656')
        hacksa_dict = crawling_url_bypage(i, '02')

    return hacksa_dict

# 학부 장학
def scholarship():
    scholarship_dict = {}

    print("학부장학-----------------------------------------------------------------------------------------------------")
    # 10페이지까지 크롤링
    for i in range(1, 3):
        driver.get('https://portal.sungshin.ac.kr/portal/ssu/menu/notice/ssuboard10.page')
        driver.switch_to.frame('IframePortlet_9616')
        scholarship_dict = crawling_url_bypage(i, '10')
    return scholarship_dict


hacksa_dict = hacksa()
for title, notice in hacksa_dict.items():
    Notice(title=title, content=notice[0], date=notice[1]).save()

scholarship_dict = scholarship()
for title, notice in scholarship_dict.items():
    Notice(title=title, content=notice[0], date=notice[1]).save()

# 포탈에서 나가기
driver.quit()