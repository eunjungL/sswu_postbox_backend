from urllib.request import urlopen
import bs4
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from postbox.models import Notice, Keyword
from urllib.request import urlopen
import bs4, datetime
from selenium import webdriver
from send_notification import send_message

# 드라이버 가져오기
desktop_driver = 'C:/Users/user/Downloads/chromedriver_win32/chromedriver.exe'
laptop_driver = 'C:/Users/dldms/Downloads/chromedriver_win32/chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(desktop_driver, options=options)


def content(a_href):
    url = a_href
    html = urlopen(url)

    bs_obj = bs4.BeautifulSoup(html.read(), "html.parser")

    # 한 공지사항에 대해 작성일, 수정일, 작성자, 조회수 가져오기-----------------------------------------
    div = bs_obj.find("div", {"class": "left"})
    dls = div.findAll("dl")

    # 작성일
    dateCreated = dls[0].find('dd').text.strip()
    dateCreated2 = datetime.datetime.strptime(dateCreated, '%Y.%m.%d')
    # 수정일
    dateModification = dls[1].find('dd').text.strip()
    # 작성자
    writer = dls[2].find('dd').text.strip()
    # 조회수
    views = dls[3].find('dd').text.strip()

    print(dateCreated)
    print(dateModification)
    print(writer)
    print(views)


    # 제목 출력-------------------------------------------------------------------------------------
    # 제목
    title = bs_obj.find('h2', {'class': 'artclViewTitle'}).text.strip()
    print(title)

    # 첨부파일 제목과 주소 가져오기--------------------------------------------------------------------
    file_dd = bs_obj.find("dd", {"class": "artclInsert"})
    files = file_dd.findAll("a", {"class": "file"})

    i = 0
    file_names = {}
    for file in files:
        # 첨부 파일 이름
        file_name = file.text.strip()
        print(file_name)
        # 첨부 파일 링크
        file_a = files[i]["href"]
        print(file_a + "\n")

        file_names[file_name] = file_a
        i = i + 1

    # 공지사항 내용-----------------------------------------------------------------------------------
    # 공지사항 본문
    notice = bs_obj.find("div", {"class": "artclView"}).text
    print(notice)

    return title, notice, dateCreated2, file_names


# 첫 번째 페이지 -> 처음부터 끝까지 모든 공지 출력
def first_page():
    i = 1
    a_artclTdTitles = driver.find_elements_by_class_name('_artclTdTitle > a')

    data = {}
    for a_artclTdTitle in a_artclTdTitles:
        a_href = a_artclTdTitle.get_attribute('href')
        print("첫 번째 페이지 " + str(i) + " 번째 공지사항--------------------------------------------------------------------")
        title, notice, date_created, file_names = content(a_href)
        notices = []
        notices.append(notice)
        notices.append(date_created)
        notices.append(file_names)
        data[title] = notices
        i = i + 1

    return data

# 페이지 클릭하기 -> 두 번째 페이지부터는 중복되는 공지사항 제외하고 출력 (n부터 m까지)
def click_page(page, n, m):
    data = {}

    i = 1
    page_temp = page
    if page == 11:
        click_next = driver.find_element_by_class_name('_next')
        click_next.click()
    else:
        if page > 11:
            page = page - 10
        click = driver.find_element_by_class_name('_inner > ul')
        click_li = click.find_elements_by_tag_name('li')
        click_li[page - 1].find_element_by_tag_name('a').click()

    a_artclTdTitles = driver.find_elements_by_class_name('_artclTdTitle > a')
    a_artclTdTitles_13 = a_artclTdTitles[n:m]
    for a_artclTdTitle in a_artclTdTitles_13:
        print(str(page_temp) + " 번째 페이지 " + str(i) + " 번째 공지사항----------------------------------------------------------------")
        a_href = a_artclTdTitle.get_attribute('href')
        title, notice, date_created, file_names = content(a_href)
        notices = []
        notices.append(notice)
        notices.append(date_created)
        notices.append(file_names)
        data[title] = notices
        i = i + 1

    return data


def hacksa():
    print("학사 공지----------------------------------------------------------------------------------------------------")
    # 학사 공지 연결
    driver.get('https://www.sungshin.ac.kr/main_kor/11107/subview.do')
    # 첫 번째 페이지 출력
    hacksa_dict = first_page()
    # 두 번째 페이지부터 20번째 페이지까지
    for i in range(2, 3):
        print(i)
        hacksa_dict.update(click_page(i, 14, 26))

    return hacksa_dict

# 일반 공지
def normal():
    print("일반 공지----------------------------------------------------------------------------------------------------")
    # 일반 공지 연결
    driver.get('https://www.sungshin.ac.kr/main_kor/11108/subview.do')
    # 첫 번째 페이지 출력
    normal_dict = first_page()
    # 두 번째 페이지부터 10번째 페이지까지
    for i in range(2, 3):
        print(i)
        normal_dict.update(click_page(i, 8, 24))

    return normal_dict

# 입학 공지
def Admission():
    print("입학 공지----------------------------------------------------------------------------------------------------")
    # 일반 공지 연결
    driver.get('https://www.sungshin.ac.kr/main_kor/11109/subview.do')
    # 첫 번째 페이지 출력
    admission_dict = first_page()
    # 두 번째 페이지부터 3번째 페이지까지
    for i in range(2, 3):
        print(i)
        admission_dict.update(click_page(i, 0, 10))

    return admission_dict

# 취업 공지
def employment():
    print("취업 공지----------------------------------------------------------------------------------------------------")
    # 일반 공지 연결
    driver.get('https://www.sungshin.ac.kr/main_kor/11116/subview.do')
    # 첫 번째 페이지 출력
    employment_dict = first_page()
    # 두 번째 페이지부터 10번째 페이지까지
    for i in range(2, 3):
        print(i)
        employment_dict.update(click_page(i, 1, 11))

    return employment_dict

# 대학원(외국인) 공지
def graduate_foreigner():
    print("대학원(외국인) 공지----------------------------------------------------------------------------------------------------")
    # 일반 공지 연결
    driver.get('https://www.sungshin.ac.kr/main_kor/17317/subview.do')
    # 첫 번째 페이지 출력
    graduate_dict = first_page()
    # 두 번째 페이지
    for i in range(2, 3):
        print(i)
        graduate_dict.update(click_page(i, 0, 10))

    return graduate_dict


hacksa_dict = hacksa()
for title, notice in hacksa_dict.items():
    notices, created = Notice.objects.get_or_create(title=title, content=notice[0], date=notice[1],
                                                    attachments=notice[2])

    keywords = Keyword.objects.all()
    if created:
        for keyword in keywords:
            if keyword.keyword in title:
                send_message(title, keyword.keyword)
        notices.save()

normal_dict = normal()
for title, notice in normal_dict.items():
    notices, created = Notice.objects.get_or_create(title=title, content=notice[0], date=notice[1],
                                                    attachments=notice[2])

    keywords = Keyword.objects.all()
    if created:
        for keyword in keywords:
            if keyword.keyword in title:
                send_message(title, keyword.keyword)
        notices.save()

admission_dict = Admission()
for title, notice in admission_dict.items():
    notices, created = Notice.objects.get_or_create(title=title, content=notice[0], date=notice[1],
                                                    attachments=notice[2])

    keywords = Keyword.objects.all()
    if created:
        for keyword in keywords:
            if keyword.keyword in title:
                send_message(title, keyword.keyword)
        notices.save()

employment_dict = employment()
for title, notice in employment_dict.items():
    notices, created = Notice.objects.get_or_create(title=title, content=notice[0], date=notice[1],
                                                    attachments=notice[2])

    keywords = Keyword.objects.all()
    if created:
        for keyword in keywords:
            if keyword.keyword in title:
                send_message(title, keyword.keyword)
        notices.save()

graduate_dict = graduate_foreigner()
for title, notice in graduate_dict.items():
    notices, created = Notice.objects.get_or_create(title=title, content=notice[0], date=notice[1],
                                                    attachments=notice[2])

    keywords = Keyword.objects.all()
    if created:
        for keyword in keywords:
            if keyword.keyword in title:
                send_message(title, keyword.keyword)
        notices.save()
