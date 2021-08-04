from pyfcm import FCMNotification
from urllib.parse import unquote, quote

APIKey = "AAAADg0BsXE:APA91bEOt7Ot39mfOCJhmzOmI86-uD557aLDNBfIJd7RCh6mmNFvsklfvUMgTsW2Xdbe5Y0_IOG8xdDZI3fo-Bvd1BOi3ZBwYb00yeFItVcBYwHKKkqrfzCZFo4bDTI3E5k48gYO3YSf"

push_service = FCMNotification(APIKey)


def send_message(title, keyword):
    data_message = {
        "body": title,
        "title": "%s 키워드에 관련된 새 공지가 있습니다." % keyword
    }

    keyword = quote(keyword, "utf8")
    result = push_service.notify_topic_subscribers(topic_name=keyword, data_message=data_message)

    print(result)
