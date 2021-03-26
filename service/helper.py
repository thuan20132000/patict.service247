import firebase_admin
from firebase_admin import credentials,messaging

import datetime
import inspect
import logging



"""
    Author:thuantruong
    created_at:24/03/2021
    desc: Use Notification of firebase FCM
"""
class Notification:

    def __init__(self,):
        self.cred = credentials.Certificate(
            "/Users/truongthuan/Develop/python/service247/local_env/vieclam24h-3d4e1-firebase-adminsdk-imaaw-daa37f2726.json")
        firebase_admin.initialize_app(self.cred)

    
    def send_notification(self,token,user,title,content,image):

        try:

            # See documentation on defining a message payload.
            message = messaging.Message(
                notification=messaging.Notification(title=title,body=content,image=image),
                token=token,
            )


            # Send a message to the device corresponding to the provided
            # registration token.
            response = messaging.send(message)
            # Response is a message ID string.
            print('Successfully sent message:', response)
            return True


        except Exception as e:
            log = Log()
            log.log_message(e)
            return False





"""
    Author:thuantruong
    created_at:24/03/2021
    desc: Use Loggin fo log file
"""
class Log:
        
    def log_message(self,message):
        log = open("/Users/truongthuan/Develop/python/service247/media/logs/logs.txt", 'a')
        # message_parse =
        func = inspect.currentframe().f_back.f_code
        co_name = func.co_name
        f_name = func.co_filename
        co_line = func.co_firstlineno

        log.write(f'\n {str(datetime.datetime.now())} : {message} at {co_line} - {co_name} - {f_name}\n')





"""
    Author:thauntruong
    created_at:26/03/2021
    desc:Use to analyze response error in api
"""
class ErrorCode:

    CANDIDATE_NOT_REGISTER = "CANDIDATE_404"
    CANDIDATE_EXIST = "CANDIDATE_201"
    
    GET_SUCCESS = "200"
    POST_SUCCESS = "201"
    UNDEFINED = "400"
    VALIDATION = "501"