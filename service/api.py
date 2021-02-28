
from rest_framework.response import Response
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions  import AllowAny,IsAuthenticated

from .models import User,Category,Job,Field,Image
from django.utils.text import slugify
from .serializers import (
    CategorySerializer,
    FieldSerializer,
    JobSerializer,
    UserSerializer,
    UserSingupSerializer,
    JobPaginationCustom,
    AuthorSerializer,
    ImageSerializer
)

import json
from django.core.serializers import serialize
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,login
from rest_framework.renderers import JSONRenderer

from rest_framework.pagination import PageNumberPagination

from django.core.paginator import Paginator

from django.core.exceptions import ObjectDoesNotExist




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





# Category API
@api_view(['GET'])
def category_list_api(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category,many=True)

    return Response(serializer.data)


@api_view(['GET'])
def category_detail_api(request,category_slug=None):
    
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
    
        serializer = CategorySerializer(category)
        return Response({
            "status":True,
            "category":serializer.data
        })

    return Response({
        "status":False,
        "category":None
    })



# Field API
@api_view(['GET'])
def field_list_api(request):
    fields = Field.objects.all()
    serializer = FieldSerializer(fields,many=True)

    return Response(serializer.data)







@api_view(['GET'])
def customer_list_api(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many=True)

    return Response(serializer.data)






# Job API

@api_view(['GET'])
def job_suggestion_api(request):
    job = Job.objects.all()
    serializer = JobSerializer
    

@api_view(['GET'])
def job_list_api(request):

    page = request.query_params.get('page')
    page_limit = request.query_params.get('limit')
    category_slug = request.query_params.get('category_slug')
    field_slug = request.query_params.get('field_slug')

    paginator = JobPaginationCustom()
    paginator.page_size = 10

    if page_limit is not None:
        paginator.page_size = int(page_limit)
    
    if category_slug is not None:
        try:
            cat = Category.objects.get(slug=category_slug)
            fields = cat.fields.all()
            jobs = Job.objects.filter(field__in=fields,status='published').order_by('-created_at').all()
            context = paginator.paginate_queryset(jobs,request)
            serializer = JobSerializer(context,many=True)
            return Response(
                paginator.get_paginated_response(serializer.data)
            )

        except Category.DoesNotExist:
            return Response({
                "status":False,
                "message":"Category is not exists"
            })

    if field_slug is not None:
        try:
            field = Field.objects.get(slug=field_slug)
            jobs = Job.objects.filter(field=field,status='published').order_by('-created_at').all()
            context = paginator.paginate_queryset(jobs,request)
            serializer = JobSerializer(context,many=True)

            return Response(paginator.get_paginated_response(serializer.data))


        except Field.DoesNotExist:
            return Response({
                "status":False,
                "message":"Field is not exists"
            })

       

    query_set = Job.objects.filter(status='published').order_by('-created_at')
    context = paginator.paginate_queryset(query_set,request)
    serializer = JobSerializer(context,many=True)

    return Response(
        paginator.get_paginated_response(serializer.data)
    )
    

@api_view(['GET'])
def job_detail_api(request,job_slug=None):


    if job_slug is not None:
        try:
            job = Job.objects.get(slug=job_slug,status='published')
            serializer = JobSerializer(job)
            
            return Response({
                "status":True,
                "data":serializer.data
            })

        except Job.DoesNotExist:
            return Response({
                "status":False,
                "data":None
            })

    
    return Response({
                "status":False,
                "data":None
            })


@api_view(['POST'])
def job_post_api(request):
    
        try:



            data = request.data
            images = list()

            if data.get('images'):
                for image in data.pop('images'):
                    image = Image.objects.create(image=image)
                    images.append(ImageSerializer(image).data)    
            job = Job()
            serializer = JobSerializer(job,data=data)
          

            if serializer.is_valid():
                job.slug = slugify(data.get('name'))
                job.name = data.get('name')
                job.suggestion_price = data.get('suggestion_price')
                job.author_id = data.get('author_id')
                job.field_id = data.get('field_id')
                job.images = images
                job.descriptions = data.get('descriptions')
                job.save()
                return Response({
                    "status":True,
                    "data":JobSerializer(job).data
                })

            return Response({
                "message":serializer.errors
            })
        except Exception as e:
            print('error: ',e)
            return Response({
                "status":False,
                "data":None,
                "message":"Please enter full of input field_id,author_id"

            })



@api_view(['PUT'])
def job_update_api(request,job_id):
    
        try:

            data = request.data
            images = list()

            job = Job.objects.get(id=job_id)

            if data.get('images'):
                for image in data.pop('images'):
                    image = Image.objects.create(image=image)
                    images.append(ImageSerializer(image).data)
                job.images = images

            job.name = data.get('name') or job.name
            job.slug = slugify(job.name)
            job.suggestion_price = data.get('suggestion_price') or job.suggestion_price
            job.field_id = data.get('field_id') or job.field_id
            job.descriptions = data.get('descriptions') or job.descriptions
            job.save()
            serializer = JobSerializer(job)
          

         
            return Response({
                "status":False,
                "data":serializer.data
            })
        except Exception as e:
            print('error: ',e)
            return Response({
                "status":False,
                "data":None,
                "message":"Please enter full of input field_id,author_id"

            })



@api_view(['DELETE'])
def job_delete_api(self,job_id):


    try:
        job = Job.objects.get(id=job_id)
        job.delete()

        return Response({
            "status":True,
            "data":None,
            "message":"Delete successfully"
        })
    except Exception as e:
         
        return Response({
            "status":False,
            "data":None,
            "message":"Delete Failed"
        
        })