from pyfcm import FCMNotification

APIKey = "AAAADg0BsXE:APA91bEOt7Ot39mfOCJhmzOmI86-uD557aLDNBfIJd7RCh6mmNFvsklfvUMgTsW2Xdbe5Y0_IOG8xdDZI3fo-Bvd1BOi3ZBwYb00yeFItVcBYwHKKkqrfzCZFo4bDTI3E5k48gYO3YSf"

push_service = FCMNotification(APIKey)


def send_message(body, title):
    data_message = {
        "body": body,
        "title": title
    }

    result = push_service.notify_topic_subscribers(topic_name="test", data_message=data_message)

    print(result)


send_message("test", "background test")