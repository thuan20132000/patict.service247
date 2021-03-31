from django.test import TestCase

# Create your tests here.

from service.firebase_notification import Notification, NotificationConfiguration


import time
import concurrent
from service.models import Job, ServiceUser, Notification as NotificationModel,CandidateUser
from service.helper import UserNotificationHandler


class JobTest:

    job_name_list = [
        'name 1',
        'name 2',
        'name 3',
        'name 4',
    ]

    user_list = list()

    def create_job_without_thread(self, name):
        start_time = time.time()

        job = Job()
        job.slug = "cacsa "
        job.name = name
        job.suggestion_price = "123"
        job.author_id = 32
        job.field_id = 2
        job.descriptions = "descriptions "
        job.save()

        image_url = "https://iso.500px.com/wp-content/uploads/2016/11/stock-photo-159533631-1500x1000.jpg"
        # notification = Notification(title=job.name,body=job.descriptions,image=image_url)
        # notification.send_topic_notification('jobpost')

        user_notification = UserNotificationHandler()
        user_list = ServiceUser.objects.all()
        # user_notification.set_user_list(user_list=user_list)
        # user_notification.handle_notification_thread(job.name,job.descriptions,image_url,job.id)

        for user in user_list:
            notification = NotificationModel()
            notification.title = job.name
            notification.user_id = user.pk
            notification.job_id = job.id
            notification.save()

        finished_time = time.time()
        print('execute with : %s user in %s' % (len(user_list), job.name))
        print("duration time without thread: ", finished_time-start_time)

    def create_job_with_thread(self, name, field_id, author_id):
        start_time = time.time()

        job = Job()
        job.slug = "cacsa "
        job.name = name
        job.suggestion_price = "120000"
        job.author_id = author_id
        job.field_id = field_id
        job.descriptions = "descriptions "
        job.location = job.location = {"address": "", "district": "Quận Liên Chiểu", "province": "Thành phố Đà Nẵng",
                                       "subdistrict": "Phường Hòa Khánh Bắc", "district_code": "490", "province_code": "48", "subdistrict_code": "20197"}
        job.save()

        image_url = "https://iso.500px.com/wp-content/uploads/2016/11/stock-photo-159533631-1500x1000.jpg"
        notification = Notification(
            title=job.name, body=job.descriptions, image=image_url)
        notification.send_topic_notification('jobpost')

        user_notification = UserNotificationHandler()
        user_list = CandidateUser.objects.all()
        user_notification.set_user_list(user_list=user_list)
        user_notification.handle_notification_thread(
            job.name, job.descriptions, image_url, job.id)

        finished_time = time.time()
        print('execute with : %s user in %s' % (len(user_list), job.name))
        print("duration time with thread: ", finished_time-start_time)

    def get_job_info(self,):
        print("job information")

    def set_user_list(self, user):

        user_list = ServiceUser.objects.all()
        self.user_list = user_list

    def get_user_list(self):

        print(self.user_list)

    def exe_with_thread(self,):
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

            for user in self.user_list:
                executor.submit(self.create_job, user.phonenumber)

        finished_time = time.time()
        print("duration with thread: %s", (finished_time-start_time))

    def exe_without_thread(self,):
        start_time = time.time()
        notification = Notification("Hello ", "Hello body")

        for user in range(5):
            self.create_job(user.username)
        finished_time = time.time()
        print("duration without thread: %s", (finished_time-start_time))


# class NotificationTest:
#     # token = "dsQNRbf9RoOvqUysJ9B_WZ:APA91bG8qW_9kkGalloK_gkXgJO-O8rj7O9bGNl1E5X9EeuThVesp8eO_2CtUUE47j-tWou5DWvFGmlBfsZJWy8LAR7uB4fpXMwg4fJwivfRcPV0Ngs_a9MB9uSuYoNROnxzeJhxrelJ"

#     try:
#         n = Notification(body="Hello content", title="Helo title", image="")
#         n.send_topic_notification('jobpost')

#     except Exception as e:
#         print("Error: ", e)

#         n = NotificationConfiguration()
#         print(n.access_token)
