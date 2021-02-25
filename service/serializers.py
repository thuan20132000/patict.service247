from rest_framework import serializers
from .models import Category,Field,Job,User



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




