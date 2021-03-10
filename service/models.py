from django.db import models
from django.contrib.auth.models import User

# Create your models here.





class Category(models.Model):


    STATUS_CHOICE = (
        ('published','PUBLISHED'),
        ('draft','DRAFT'),
        ('pending','PENDING')
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)

    image = models.ImageField(upload_to='upload/')
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
        ('confirmed','CONFIRMED'),
    )

    name = models.CharField(max_length=220)
    slug = models.SlugField(max_length=220)
    descriptions = models.TextField(blank=True,null=True)
    suggestion_price = models.DecimalField(max_digits=18,decimal_places=2)
    location = models.JSONField(blank=True,null=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICE,default='published')

    author = models.ForeignKey(
        User,
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
    
    STATUS_CHOICE = (
        ('published','PUBLISHED'),
        ('draft','DRAFT'),
        ('pending','PENDING'),
        ('approved','APPROVED'),
        ('confirmed','CONFIRMED'),

    )

    expected_price = models.DecimalField(max_digits=18,decimal_places=2,null=True)
    descriptions = models.TextField(null=True)
    confirmed_price = models.DecimalField(max_digits=18,decimal_places=2,null=True)
    time_start = models.DateTimeField(null=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICE,default='published')

    
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='jobcandidate'
    )

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='usercandidate'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




    def __str__(self,):
        return "Job candidate"

class Review(models.Model):

    STATUS_CHOICE = (
        ('published','PUBLISHED'),
        ('draft','DRAFT'),
        ('pending','PENDING'),
    )

    review_level = models.IntegerField()
    review_content = models.TextField(null=True)
    review_images = models.JSONField(blank=True)

    job_candidate = models.ForeignKey(
        JobCandidate,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    status = models.CharField(max_length=10,choices=STATUS_CHOICE,default='published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self,):
        return self.review_content





    
class CandidateUser(models.Model):
    STATUS_CHOICE = (
        ('published','PUBLISHED'),
        ('draft','DRAFT'),
    )
    is_candidate = models.BooleanField(default=False)
    category = models.ManyToManyField(Category,blank=True,null=True)
    fields = models.ManyToManyField(Field,blank=True,null=True)
    location = models.JSONField(blank=True,null=True)


    user = models.OneToOneField(
        User,
        related_name="candidate_user",
        on_delete=models.CASCADE,
        primary_key=True,
        unique=True
    )

    status = models.CharField(max_length=10,choices=STATUS_CHOICE,default='published')


    def __str__(self,):
    
        return f"candidate_user {self.user}"


class Image(models.Model):
    STATUS_CHOICE = (
        ('published','PUBLISHED'),
        ('draft','DRAFT'),
    )

    image = models.ImageField(upload_to='upload/')
    image_type = models.CharField(max_length=20,null=True)
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


    status = models.CharField(max_length=10,choices=STATUS_CHOICE,default='published')
