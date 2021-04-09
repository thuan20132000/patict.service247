import firebase_admin
from firebase_admin import credentials, messaging

import datetime
import inspect
import logging
import concurrent
from service.models import Notification as NotificationModel,ServiceUser
from django.contrib.admin import SimpleListFilter

"""
    Author:thuantruong
    created_at:24/03/2021
    desc: Use Notification of firebase FCM
"""


class Notification:

    def __init__(self,):
        self.cred = credentials.Certificate(
            "/Users/truongthuan/Develop/python/service247/local_env/fcm_key.json")
        firebase_admin.initialize_app(self.cred)

    def send_notification(self, token, user, title, content, image):

        try:

            # See documentation on defining a message payload.
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title, body=content, image=image),
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

    def send_to_one(self, user_id, title, content, image):
        try:

            message = messaging.Message(
                data={
                    'score': '850',
                    'time': '2:45',
                },
                token=registration_token,
            )
            response = messaging.send(message)
            # Response is a message ID string.
            print('Successfully sent message:', response)

        except Exception as e:
            log = Log()
            log.log_message(e)
            return False

    def get_user_token(self, user_id):

        try:

            user = ServiceUser.objects.get(pk=user_id)
            print(user)
            

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

    def log_message(self, message):
        log = open(
            "/Users/truongthuan/Develop/python/service247/media/logs/logs.txt", 'a')
        # message_parse =
        func = inspect.currentframe().f_back.f_code
        co_name = func.co_name
        f_name = func.co_filename
        co_line = func.co_firstlineno

        log.write(
            f'\n {str(datetime.datetime.now())} : {message} at {co_line} - {co_name} - {f_name}\n')


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


"""
    Author:thuantruong
    created_at:30/03/2021
    desc: Use to save other user notification after having a job post
"""


class UserNotificationHandler:

    user_list = list()

    def get_user_list(self,):
        return self.user_list

    def set_user_list(self, user_list=list()):
        self.user_list = user_list

    def print_user_list(self,):
        print("user list: ", self.user_list)

    def insert_user_notification(self, title, user_id, job_id):
        notification = NotificationModel()
        notification.title = title
        # notification.content = content
        notification.user_id = user_id
        notification.job_id = job_id
        notification.save()

    def handle_notification_thread(self, title, body, image_url, job_id):

        if len(self.user_list) < 0:
            return

        user_list = self.user_list

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for user in user_list:
                future = executor.submit(
                    self.insert_user_notification, title, user.pk, job_id)


class ValidationInput:


    def __init__(self,*valid_data):
        self.input_data = list()
        for x in valid_data:
            self.input_data.append(x)


    def is_valid(self,):
        for x in self.input_data:
            if x is None or len(x) < 10:
                return False
        return True





class JSONFieldFilter(SimpleListFilter):
    """
    """

    def __init__(self, *args, **kwargs):

        super(JSONFieldFilter, self).__init__(*args, **kwargs)

        assert hasattr(self, 'title'), (
            'Class {} missing "title" attribute'.format(self.__class__.__name__)
        )
        assert hasattr(self, 'parameter_name'), (
            'Class {} missing "parameter_name" attribute'.format(self.__class__.__name__)
        )
        assert hasattr(self, 'json_field_name'), (
            'Class {} missing "json_field_name" attribute'.format(self.__class__.__name__)
        )
        assert hasattr(self, 'json_field_property_name'), (
            'Class {} missing "json_field_property_name" attribute'.format(self.__class__.__name__)
        )

    def lookups(self, request, model_admin):
        """
        # Improvemnt needed: if the size of jsonfield is large and there are lakhs of row
        """
        if '__' in self.json_field_property_name:  # NOTE: this will cover only one nested level
            keys = self.json_field_property_name.split('__')
            field_value_set = set(
                data[keys[0]][keys[1]] for data in model_admin.model.objects.values_list(self.json_field_name, flat=True)
            )
        else:
            field_value_set = set(
                data[self.json_field_property_name] for data in model_admin.model.objects.values_list(self.json_field_name, flat=True)
            )
        return [(v, v) for v in field_value_set]

    def queryset(self, request, queryset):
        if self.value():
            json_field_query = {"{}__{}".format(self.json_field_name, self.json_field_property_name): self.value()}
            return queryset.filter(**json_field_query)
        else:
            return queryset


