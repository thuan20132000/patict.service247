
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions  import AllowAny,IsAuthenticated

from .models import User,Category,Job,Field

from .serializers import CategorySerializer,FieldSerializer,JobSerializer,UserSerializer,UserSingupSerializer
import json
from django.core.serializers import serialize
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,login
from rest_framework.renderers import JSONRenderer

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }



@api_view(['GET'])
def category_list(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category,many=True)

    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
   
    serializer = UserSingupSerializer(data=request.data)



    if serializer.is_valid():
        user = serializer.create(validated_data=request.data)
        user.save()
        return Response({
            "status":True,
            "user": UserSingupSerializer(user).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

    return Response({
        "status":False,
        "error_messages":serializer.errors
    })



@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):


    try:
        serializer = UserSerializer(data=request.data)
     
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(username=username,password=password)

            if user is not None:
                
                refresh = RefreshToken.for_user(user)
                return Response({
                    "status":True,
                    "user":UserSerializer(user).data,
                    "refresh":str(refresh),
                    "access":str(refresh.access_token)
                })

            else:
                return Response({
                    "status":False,
                    "user":None,
                    "message":"Please check username and password correctly!"
                })

        else:
            return Response({
                "status":False,
                "error":serializer.errors
            })

    
        return Response({
            "status":False,
            "user":None
        })

    
    except Exception as error:

        return Response({
            "status":False,
            "error":error
        })






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


@api_view(['GET'])
def customer_list_api(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many=True)

    return Response(serializer.data)

