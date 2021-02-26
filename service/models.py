from django.db import models
from django.contrib.auth.models import User

# Create your models here.




# class Image(models.Model):
#     STATUS_CHOICE = (
#         ('published','PUBLISHED'),
#         ('draft','DRAFT'),
#     )

#     image_url = models.TextField()
#     status = models.CharField(max_length=10,choices=STATUS_CHOICE,default='published')







class Category(models.Model):


    STATUS_CHOICE = (
        ('published','PUBLISHED'),
        ('draft','DRAFT'),
        ('pending','PENDING')
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)

    image = models.ImageField(upload_to='upload/',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICE,default='published')

    def __str__(self,):
        return self.name





class Field(models.Model):
    STATUS_CHOICE = (
        ('published','PUBLISHED'),
        ('draft','DRAFT'),
        ('pending','PENDING'),
    )


    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='upload/',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICE,default='published')

    category = models.ForeignKey(
        Category,
        related_name='fields',
        on_delete=models.CASCADE
    )

    def __str__(self,):
        return self.name



class Job(models.Model):
    STATUS_CHOICE = (
        ('published','PUBLISHED'),
        ('draft','DRAFT'),
        ('pending','PENDING'),
    )

    name = models.CharField(max_length=220)
    slug = models.SlugField(max_length=220)
    images = models.JSONField(blank=True,null=True)
    descriptions = models.TextField(blank=True,null=True)
    suggestion_price = models.DecimalField(max_digits=18,decimal_places=2)
    location = models.JSONField(blank=True,null=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICE,default='published')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='jobs'
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





class JobCollaborator(models.Model):
    
    STATUS_CHOICE = (
        ('published','PUBLISHED'),
        ('draft','DRAFT'),
        ('pending','PENDING'),
    )

    expected_price = models.DecimalField(max_digits=18,decimal_places=2)
    description = models.TextField(null=True)
    confirmed_price = models.DecimalField(max_digits=18,decimal_places=2)
    time_start = models.DateTimeField(null=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICE,default='published')

    
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='job_collaborator'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self,):
        return self.job

class Review(models.Model):

    STATUS_CHOICE = (
        ('published','PUBLISHED'),
        ('draft','DRAFT'),
        ('pending','PENDING'),
    )

    review_level = models.IntegerField()
    review_content = models.TextField(null=True)
    review_images = models.JSONField(blank=True)

    job_collaborator = models.ForeignKey(
        JobCollaborator,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    status = models.CharField(max_length=10,choices=STATUS_CHOICE,default='published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self,):
        return self.review_content