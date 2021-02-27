from rest_framework import serializers
from .models import Category,Field,Job,User
from django.conf import settings
from rest_framework.pagination import PageNumberPagination,BasePagination

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id','name','image','status','slug']


  


class FieldSerializer(serializers.ModelSerializer):


    class Meta:
        model = Field
        fields = ['id','name','image','status','slug']






class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields  = ['id','name','images','status','descriptions','suggestion_price','author','field','created_at']



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






