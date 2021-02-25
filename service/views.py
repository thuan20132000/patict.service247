from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from .models import Category,Field,Job,User

from .serializers import CategorySerializer,FieldSerializer,JobSerializer,UserSerializer



@api_view(['GET'])
def category_list_api(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category,many=True)

    return Response(serializer.data)



@api_view(['GET'])
def field_list_api(request):
    fields = Field.objects.all()
    serializer = FieldSerializer(fields,many=True)

    return Response(serializer.data)



@api_view(['GET'])
def job_list_api(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs,many=True)

    return Response(serializer.data)



@api_view(['POST'])
def user_signup(request):
    serializer = UserSerializer(data=request.data)

    
    if serializer.is_valid():
        user = serializer.create(validated_data=request.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# def user_signin(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.



@api_view(['PUT'])
def user_update(request,customer_id):

    try:
        user = User.objects.get(id=customer_id)
        serializer = UserSerializer(instance=user,data=request.data)

        if serializer.is_valid():
            user_update =  serializer.update(instance=user,validated_data=request.data)
            return Response(data=serializer.data,status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    except user.DoesNotExist:
        return Response(data="error",status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def customer_list_api(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many=True)

    return Response(serializer.data)


# def user_signin(request):
#     serializer = UserSerializer(data=request.data)
            


