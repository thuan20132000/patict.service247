from django.db import models
from django.contrib.auth.models import User

# Create your models here.




class Image(models.Model):
    STATUS_CHOICE = (
        ('published','PUBLISHED'),
        ('draft','DRAFT'),
    )

    image_url = models.TextField()
    status = models.CharField(choices=STATUS_CHOICE,default='published')



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
    status = models.CharField(choices=STATUS_CHOICE,default='published')

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
    status = models.CharField(choices=STATUS_CHOICE,default='published')

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
    images = models.JSONField(blank=True)
    descriptions = models.TextField(null=True)
    suggestion_price = models.DecimalField(18,2)
    location = models.JSONField(blank=True)
    status = models.CharField(choices=STATUS_CHOICE,default='published')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job'
    )
    occupations = models.JSONField(blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
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
    status = models.CharField(choices=STATUS_CHOICE)

    
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='job_collaborator'
    )




class Review(models.Model):

    STATUS_CHOICE = (
        ('published','PUBLISHED'),
        ('draft','DRAFT'),
        ('pending','PENDING'),
    )

    review_level = models.IntegerField(max_length=5)
    review_content = models.TextField(null=True)
    review_images = models.JSONField(blank=True)

    job_collaborator = models.ForeignKey(
        JobCollaborator,
        on_delete=models.CASCADE,
        related_name='review'
    )

    status = models.CharField(choices=STATUS_CHOICE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    