
from .models import Category, Field, Job, ServiceUser
from faker import Faker
import random
from service.helper import Log

fake = Faker()


def gen_users():
    phonenumber_list = ['0982527982',
                        '0917749254', '0904770053', '0974880788', '0983888611']
    log = Log()

    try:

        for i in range(len(phonenumber_list)):
            user = ServiceUser()
            user.username = fake.name()
            user.phonenumber = phonenumber_list[i]
            user.set_password("Thuan123")
            user.save()
        message = f'Success: gen_users'
        log.log_message(message)

    except Exception as e:
        message = f'Error: {e}'
        print(message)
        log.log_message(message)


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
            job.field = random.choice(fields)
            job.save()
        message = f'Success: gen_category'
        log.log_message(message)
    except Exception as e:
        message = f'Error: {e}'
        print(message)
        log = Log()
        log.log_message(message)
