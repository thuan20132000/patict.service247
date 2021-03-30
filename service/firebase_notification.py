import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from local_env.config import FILE_PATH

class NotificationConfiguration:

    # path = "/Users/truongthuan/Develop/python/service247/local_env/fcm_key.json"
    # self.cred = credentials.Certificate(path)
    # self.default_app = firebase_admin.initialize_app(self.cred)
    # self.access_token = self.cred.get_access_token().access_token


    def __init__(self,):    
        path = FILE_PATH+"/local_env/fcm_key.json"
        self.cred = credentials.Certificate(path)
        self.default_app = firebase_admin.initialize_app(self.cred,options={'projectId':'vieclam24h-3d4e1'})
        self.access_token = self.cred.get_access_token().access_token



class Notification(NotificationConfiguration):

    def __init__(self, title, body, image=None):
        self.title = title
        self.body = body
        self.image = image
        
        if not firebase_admin._apps:
            NotificationConfiguration()

        
        
    def send_topic_notification(self, topic):
        message = messaging.Message(
            notification=messaging.Notification(
                title=self.title, body=self.body, image=self.image),
            topic=topic
        )
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
        
