from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, AbstractUser
from django.urls import reverse
# Create your models here.
# Preparing to transfer from User to ServiceUser


class ServiceUser(AbstractBaseUser):

    STATUS_CHOICE = (
        ('published', 'PUBLISHED'),
        ('draft', 'DRAFT'),
        ('pending', 'PENDING')
    )

    phonenumber = models.CharField(max_length=16, null=None,unique=True)
    age = models.IntegerField(max_length=120, null=True)
    username = models.CharField(max_length=255)
    gender = models.CharField(max_length=25, null=True)
    profile_image = models.ImageField(upload_to='upload/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default='published')

    notification_token = models.TextField(blank=True,null=True)

    REQUIRED_FIELDS = ['phonenumber']

    def __str__(self,):
        return "Service User:  %s %s "% (self.username,self.phonenumber)


    def get_absolute_url(self,):
        return '/admin/service/serviceuser/%i'%self.pk



class Category(models.Model):

    STATUS_CHOICE = (
        ('published', 'PUBLISHED'),
        ('draft', 'DRAFT'),
        ('pending', 'PENDING')
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    image = models.ImageField(upload_to='upload/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default='published')

    def __str__(self,):
        return self.name


class Field(models.Model):
    STATUS_CHOICE = (
        ('published', 'PUBLISHED'),
        ('draft', 'DRAFT'),
        ('pending', 'PENDING'),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='upload/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default='published')

    category = models.ForeignKey(
        Category,
        related_name='fields',
        on_delete=models.CASCADE
    )

    def __str__(self,):
        return self.name


class Job(models.Model):
    STATUS_CHOICE = (
        ('published', 'PUBLISHED'),
        ('draft', 'DRAFT'),
        ('pending', 'PENDING'),
        ('approved', 'APPROVED'),
        ('confirmed', 'CONFIRMED'),
    )

    name = models.CharField(max_length=220)
    slug = models.SlugField(max_length=220)
    descriptions = models.TextField(blank=True, null=True)
    suggestion_price = models.DecimalField(max_digits=18, decimal_places=2)
    location = models.JSONField(blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default='published')
    immidiately = models.BooleanField(null=True, default=False)
    worktime = models.DateTimeField(null=True, blank=True)

    author = models.ForeignKey(
        ServiceUser,
        on_delete=models.CASCADE,
        related_name='jobs',
    )

    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self,):
        return self.name


class JobCandidate(models.Model):

    STATUS_LIST = ['published', 'cancel', 'pending', 'approved', 'confirmed']
    STATUS_CHOICE = (
        (STATUS_LIST[0], 'PUBLISHED'),
        (STATUS_LIST[1], 'CANCEL'),
        (STATUS_LIST[2], 'PENDING'),
        (STATUS_LIST[3], 'APPROVED'),
        (STATUS_LIST[4], 'CONFIRMED'),

    )

    expected_price = models.DecimalField(
        max_digits=18, decimal_places=2, null=True)
    descriptions = models.TextField(null=True)
    confirmed_price = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True)
    time_start = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default='published')

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='jobcandidate'
    )

    candidate = models.ForeignKey(
        ServiceUser,
        on_delete=models.CASCADE,
        related_name='usercandidate'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self,):
        return "Job candidate"


class Review(models.Model):

    STATUS_CHOICE = (
        ('published', 'PUBLISHED'),
        ('draft', 'DRAFT'),
        ('pending', 'PENDING'),
    )

    review_level = models.IntegerField(null=True, default=0)
    review_content = models.TextField(null=True)

    job_candidate = models.ForeignKey(
        JobCandidate,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True
    )

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default='published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self,):
        return self.review_content


class CandidateUser(models.Model):
    STATUS_CHOICE = (
        ('published', 'PUBLISHED'),
        ('draft', 'DRAFT'),
    )
    is_candidate = models.BooleanField(default=False)
    category = models.ManyToManyField(Category, blank=True, null=True)
    fields = models.ManyToManyField(Field, blank=True, null=True)
    location = models.JSONField(blank=True, null=True)
    descriptions = models.TextField(blank=True, null=True, default=None)

    user = models.OneToOneField(
        ServiceUser,
        related_name="candidate_user",
        on_delete=models.CASCADE,
        primary_key=True,
        unique=True
    )

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default='published')

    def __str__(self,):

        return f"candidate_user {self.user}"


class Image(models.Model):
    STATUS_CHOICE = (
        ('published', 'PUBLISHED'),
        ('draft', 'DRAFT'),
    )

    image = models.ImageField(upload_to='upload/')
    image_type = models.CharField(max_length=20, null=True)
    candidate_user = models.ForeignKey(
        CandidateUser,
        on_delete=models.CASCADE,
        null=True,
        related_name="candidate_user"
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        null=True,
        related_name="jobs"
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.SET_NULL,
        null=True,
        related_name="review"
    )

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default='published')


class Notification(models.Model):
    STATUS_CHOICE = (
        ('published', 'PUBLISHED'),
        ('draft', 'DRAFT'),
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default='published')

    title = models.CharField(max_length=255, null=True)
    content = models.TextField(null=True)
    image = models.ImageField(upload_to='upload/', blank=True)
    topic = models.CharField(max_length=255, null=True)
    user_id = models.ForeignKey(
        ServiceUser,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
