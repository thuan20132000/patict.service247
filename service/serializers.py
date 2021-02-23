from rest_framework import serializers
from .models import Category,Field,Job



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
        fields  = ['id','name','images','status','descriptions','suggestion_price','author','field']