from urllib.request import urlopen
import bs4
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from postbox.models import Notice

url = "https://www.sungshin.ac.kr/main_kor/11108/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGbWFpbl9rb3IlMkYzMTgyJTJGMTAzMTc1JTJGYXJ0Y2xWaWV3LmRvJTNGcGFnZSUzRDElMjZzcmNoQ29sdW1uJTNEJTI2c3JjaFdyZCUzRCUyNmJic0NsU2VxJTNEJTI2YmJzT3BlbldyZFNlcSUzRCUyNnJnc0JnbmRlU3RyJTNEJTI2cmdzRW5kZGVTdHIlM0QlMjZpc1ZpZXdNaW5lJTNEZmFsc2UlMjZwYXNzd29yZCUzRCUyNg%3D%3D"
html = urlopen(url)

bs_obj = bs4.BeautifulSoup(html.read(), "html.parser")

# 한 공지사항에 대해 작성일, 수정일, 작성자, 조회수 가져오기-----------------------------------------
div = bs_obj.find("div", {"class": "left"})
dls = div.findAll("dl")

# 작성일
dateCreated = dls[0].find('dd').text.strip()
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

#제목 출력-------------------------------------------------------------------------------------
# 제목
title = bs_obj.find('h2', {'class': 'artclViewTitle'}).text.strip()
print(title)

#첨부파일 제목과 주소 가져오기--------------------------------------------------------------------
file_dd = bs_obj.find("dd", {"class": "artclInsert"})
files = file_dd.findAll("a", {"class": "file"})

i = 0
for file in files:
    file_name = file.text
    print(file_name.strip())
    file_a = files[i]["href"]
    print(file_a + "\n")
    i = i + 1
#----------------------------------------------------------------------------------------------

# 공지사항 내용
notice = bs_obj.find("div", {"class": "artclView"}).text
print(notice)


if __name__=='__main__':
    Notice(title=title, content=notice).save()
