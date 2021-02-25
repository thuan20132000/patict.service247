
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework import status

from .models import User,Category,Job,Field

from .serializers import CategorySerializer,FieldSerializer,JobSerializer,UserSerializer
import json
from django.core.serializers import serialize

@api_view(['GET'])
def category_list(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category,many=True)

    return Response(serializer.data)



@api_view(['POST'])
def signup(request):
   
    serializer = UserSerializer(data=request.data)



    if serializer.is_valid():
        user = serializer.create(validated_data=request.data)
        user.save()
        return Response({
            "user": UserSerializer(user).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

    return Response({
        "status":False,
        "error_messages":serializer.errors
    })

def login(request):

    serialize = UserSerializer(data=request.data)
    