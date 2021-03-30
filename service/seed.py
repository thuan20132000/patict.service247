
from .models import Category, Field, Job, ServiceUser
from faker import Faker
import random
from service.helper import Log
import concurrent
import time

fake = Faker()
log = Log()


def gen_users_without_thread(number):
    phonenumber_list = ['0982527982',
                        '0917749254', '0904770053', '0974880788', '0983888611']

    try:
        start_time = time.time()

        for i in range(number):
            user = ServiceUser()
            user.username = fake.name()
            user.phonenumber = fake.msisdn()
            user.set_password("Thuan123")
            user.save()

        finished_time = time.time()
        message = f'Success: gen_users in {finished_time - start_time}'
        log.log_message(message)
        print(message)

    except Exception as e:
        message = f'Error: {e}'
        print(message)
        log.log_message(message)


def gen_users_with_thread(number):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for x in range(number):
            future = executor.submit(
                insert_user, fake.msisdn(), fake.name(), "Thuan123")
            # print('Thread: ', x)
            # print("result: ", future.result())
    finished_time = time.time()
    message = f'Success: gen_users in {finished_time - start_time}'
    log.log_message(message)
    print(message)


def insert_user(phonenumber, username, password):

    user = ServiceUser()
    user.username = username
    user.phonenumber = phonenumber
    user.set_password(password)
    user.save()


def gen_category():
    category_list = [
        {
            "name": "Điện",
            "slug": "dien-dien-tu",
        },
        {
            "name": "Khoá",
            "slug": "khoa",
        },
        {
            "name": "Giao hàng",
            "slug": "giao-hang",
        },
        {
            "name": "Y tế",
            "slug": "y-te",
        },
        {
            "name": "Nội thất",
            "slug": "noi-that",
        },
        {
            "name": "Xây dựng",
            "slug": "xay-dung",
        },
    ]
    log = Log()

    try:

        for c in category_list:
            cat = Category()
            cat.name = c.get('name')
            cat.slug = c.get('slug')
            cat.save()

        message = f'Success: gen_category'
        log.log_message(message)

    except Exception as e:
        message = f'Error: {e}'
        print(message)
        log.log_message(message)


def gen_field(number):
    log = Log()

    try:
        cat = Category.objects.all()
        # random_items = random.sample(cat,6)
        for i in range(number):
            field = Field()
            field.name = fake.name()
            field.slug = fake.slug()
            field.category = random.choice(cat)
            field.save()
        message = f'Success: gen_field'
        log.log_message(message)
    except Exception as e:
        message = f'Error: {e}'
        print(message)
        log.log_message(message)


def gen_jobs(number):
    log = Log()

    try:
        fields = Field.objects.all()
        users = ServiceUser.objects.all()

        for i in range(number):
            job = Job()
            job.name = fake.job()
            job.slug = fake.slug()
            job.descriptions = fake.name()
            job.suggestion_price = random.randint(1000, 2000)
            job.author = random.choice(users)
            job.location = {"address": "", "district": "Quận Liên Chiểu", "province": "Thành phố Đà Nẵng",
                            "subdistrict": "Phường Hòa Khánh Bắc", "district_code": "490", "province_code": "48", "subdistrict_code": "20197"}
            job.field = random.choice(fields)
            job.save()
        message = f'Success: gen_category'
        log.log_message(message)
    except Exception as e:
        message = f'Error: {e}'
        print(message)
        log = Log()
        log.log_message(message)
