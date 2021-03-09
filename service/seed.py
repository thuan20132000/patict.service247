
from .models import Category,Field,Job,User
from faker import Faker
import random


fake = Faker()



def gen_users(number):

    for i in range(number):
        user = User()
        user.username = fake.name()
        user.email = fake.email()
        user.password = f"{number}{fake.name()}"
        user.save()


def gen_category(number):
    
    for i in range(number):
        cat = Category()
        cat.name = fake.name()
        cat.slug = fake.slug()
        cat.save()




def gen_field(number):

    cat = Category.objects.all()
    # random_items = random.sample(cat,6)

    for i in range(number):
        field = Field()
        field.name = fake.name()
        field.slug = fake.slug()
        field.category = random.choice(cat)
        field.save()




def gen_jobs(number):

    fields = Field.objects.all()
    users = User.objects.all()

    for i in range(number):
        job = Job()
        job.name = fake.job()
        job.slug = fake.slug()
        job.descriptions = fake.name()
        job.suggestion_price = random.randint(1000,2000)
        job.author = random.choice(users)
        job.field = random.choice(fields)
        job.save()
