from rest_framework import serializers
from .models import Category,Field,Job,User,Image
from django.conf import settings
from rest_framework.pagination import PageNumberPagination,BasePagination

from django.utils.text import slugify
from django.core.exceptions import FieldDoesNotExist

class UserSingupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self,validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            
        )
        user.set_password(validated_data['password'])
        return user



class UserSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()


    class Meta:
        model = User
        fields = '__all__'
        

    def update(self,instance,validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.email = validated_data.get('email',instance.email)
        instance.save()
        return instance






class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','email']


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id','name','image','status','slug']


  


class FieldSerializer(serializers.ModelSerializer):

    

    class Meta:
        model = Field
        fields = ['id','name','image','status','slug']






class JobSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    suggestion_price = serializers.DecimalField(required=True,decimal_places=2,max_digits=18)
    # field_id = serializers.IntegerField(required=True)
    slug = serializers.SlugField(required=False)
    class Meta:
        model = Job
        depth = 1
        fields  = ['id','name','slug','images','location','status','descriptions','suggestion_price','author','field','created_at']
    
    def create(self,validated_data):
        job = Job()
        job.name = validated_data['name']
        job.slug = validated_data['slug']
        job.suggestion_price = validated_data['suggestion_price']
        job.author = validated_data['author']
        job.field = validated_data['field']
        return job

    def create_new_job(self,validated_data):
        # print(validated_data)

        
           
        job = Job()
        job.name = validated_data.get('name')
        job.slug = slugify(validated_data.get('name'))
        job.suggestion_price = validated_data['suggestion_price']
        job.author_id = validated_data['author_id']
        job.field_id = validated_data['field_id']
        images = validated_data.pop('images')
        for image in images:
            image = Image.objects.create(image_url=image,job_id=job.id)
            print('image: ',image)

        return job        
         
    
   

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id','image','status']




class JobPaginationCustom(PageNumberPagination):
    

    def get_paginated_response(self,data):
        return {
            "status":True,
            'count':self.page.paginator.count,
            'next':self.get_next_link(),
            'previous':self.get_previous_link(),
            'limit':self.page_size,
            'data':data,
        }

    
    

