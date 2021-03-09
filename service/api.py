
from rest_framework.response import Response
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import (
    User,
    Category,
    Job,
    Field,
    Image,
    JobCandidate,
    CandidateUser
)
from django.utils.text import slugify
from .serializers import (
    CategorySerializer,
    FieldSerializer,
    JobSerializer,
    UserSerializer,
    UserSingupSerializer,
    JobPaginationCustom,
    AuthorSerializer,
    ImageSerializer,
    JobCandidateSerializer,
    PaginationBaseCustom,
    CandidateUserSerializer
)

import json
from django.core.serializers import serialize
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from rest_framework.renderers import JSONRenderer

from rest_framework.pagination import PageNumberPagination

from django.core.paginator import Paginator

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


@permission_classes([AllowAny])
@api_view(['GET'])
def category_list(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)

    return Response(serializer.data)


# User API
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):

    serializer = UserSingupSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.create(validated_data=request.data)
        user.save()
        return Response({
            "status": True,
            "user": UserSingupSerializer(user).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

    return Response({
        "status": False,
        "error_messages": serializer.errors
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):

    try:
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:

                refresh = RefreshToken.for_user(user)

                return Response({
                    "status": True,
                    "user": UserSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    # "candidate_info":candidate_info
                })

            else:
                return Response({
                    "status": False,
                    "user": None,
                    "message": "Please check username and password correctly!"
                })

        else:
            return Response({
                "status": False,
                "error": serializer.errors
            })

        return Response({
            "status": False,
            "user": None
        })

    except Exception as error:

        return Response({
            "status": False,
            "error": error
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def register_candidate_api(request, user_id):
    try:

        data = request.data
        images = list()
        location = list()
        categories = list()
        fields = list()

        if data.get('location'):
            location_str = data.get('location')
            location = json.loads(location_str)
        if data.get('categories'):
            categories_str = data.get('categories')
            categories = json.loads(categories_str)
        if data.get('fields'):
            fields_str = data.get('fields')
            fields = json.loads(fields_str)

        user_id = data.get('user') or None

        candidate_user = CandidateUser()
        serializer = CandidateUserSerializer(candidate_user, data=data)

        if serializer.is_valid():

            candidate_user.is_candidate = True
            candidate_user.user_id = user_id
            candidate_user.category.set(categories)
            candidate_user.fields.set(fields)
            candidate_user.location = location
            candidate_user.save()

            if data.get('images_file'):
                for image in data.pop('images_file'):
                    image = Image.objects.create(
                        image=image, image_type="identification", candidate_user=candidate_user)
                    images.append(ImageSerializer(image).data)

            return Response({
                "status": True,
                "data": CandidateUserSerializer(candidate_user).data,
            })

        return Response({
            "status": False,
            "data": None,
            "error": serializer.errors
        })

    except Exception as e:
        print('error: ', e)
        return Response({
            "status": False,
            "data": None,
            "message": "Please enter full of input field_id,author_id"

        })


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_candidate_api(request, user_id):
    try:

        data = request.data
        images = list()
        location = list()
        categories = list()
        fields = list()

        if data.get('location'):
            location_str = data.get('location')
            location = json.loads(location_str)
        if data.get('categories'):
            categories_str = data.get('categories')
            categories = json.loads(categories_str)
        if data.get('fields'):
            fields_str = data.get('fields')
            fields = json.loads(fields_str)

        user_id = data.get('user') or None

        candidate_user = CandidateUser.objects.get(user_id=user_id)

        if categories:
            candidate_user.category.set(categories)
        if fields:
            candidate_user.fields.set(fields)
        if location:
            candidate_user.location = location
        if data.get('images_file'):
            Image.objects.filter(
                candidate_user=candidate_user).update(status='draft')
            # print(candidate_user_images)
            for image in data.pop('images_file'):
                image = Image.objects.create(
                    image=image, image_type="identification", candidate_user=candidate_user)
                images.append(ImageSerializer(image).data)
        candidate_user.save()

        return Response({
            "status": True,
            "message": "Success",
            "data": CandidateUserSerializer(candidate_user).data,
        })

    except Exception as e:
        print('error: ', e)
        return Response({
            "status": False,
            "data": None,
            "message": "Something went wrong!!"

        })


# Category API
@api_view(['GET'])
def category_list_api(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def category_detail_api(request, category_slug=None):

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)

        serializer = CategorySerializer(category)
        return Response({
            "status": True,
            "category": serializer.data
        })

    return Response({
        "status": False,
        "category": None
    })


# Field API
@api_view(['GET'])
def field_list_api(request):

    category_id = request.query_params.get('category_id')

    if category_id is not None:
        fields = Field.objects.filter(category__id=category_id)
    else:
        fields = Field.objects.all()

    serializer = FieldSerializer(fields, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def field_detail_api(request, field_id):
    field = Field.objects.get(id=field_id)
    print('field: ', field.jobs.all())

    serializer = FieldSerializer(field)
    return Response(serializer.data)


@api_view(['GET'])
def customer_list_api(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

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
            jobs = Job.objects.filter(
                field__in=fields, status='published').order_by('-created_at').all()
            context = paginator.paginate_queryset(jobs, request)
            serializer = JobSerializer(context, many=True)
            return Response(
                paginator.get_paginated_response(serializer.data)
            )

        except Category.DoesNotExist:
            return Response({
                "status": False,
                "message": "Category is not exists"
            })

    if field_slug is not None:
        try:
            field = Field.objects.get(slug=field_slug)
            jobs = Job.objects.filter(
                field=field, status='published').order_by('-created_at').all()
            context = paginator.paginate_queryset(jobs, request)
            serializer = JobSerializer(context, many=True)

            return Response(paginator.get_paginated_response(serializer.data))

        except Field.DoesNotExist:
            return Response({
                "status": False,
                "message": "Field is not exists"
            })

    query_set = Job.objects.filter(status='published').order_by('-created_at')
    context = paginator.paginate_queryset(query_set, request)
    serializer = JobSerializer(context, many=True)

    return Response(
        paginator.get_paginated_response(serializer.data)
    )


@api_view(['GET'])
def job_detail_api(request, job_id=None):

    if job_id is not None:
        try:
            job = Job.objects.get(id=job_id, status='published')
            serializer = JobSerializer(job)

            # print('job candidates: ',job.jobcandidate.all())

            return Response({
                "status": True,
                "data": serializer.data
            })

        except Job.DoesNotExist:
            return Response({
                "status": False,
                "data": None
            })

    return Response({
        "status": False,
        "data": None
    })


@api_view(['POST'])
def job_post_api(request):

    try:

        data = request.data
        images = list()
        location = list()

        if data.get('location'):
            location_str = data.get('location')
            location = json.loads(location_str)

        job = Job()
        serializer = JobSerializer(job, data=data)

        if serializer.is_valid():

            job.slug = slugify(data.get('name'))
            job.name = data.get('name')
            job.suggestion_price = data.get('suggestion_price')
            job.author_id = data.get('author_id')
            job.field_id = data.get('field_id')
            job.descriptions = data.get('descriptions')
            job.location = location
            job.save()

            if data.get('images_file'):
                for image in data.pop('images_file'):
                    image = Image.objects.create(
                        image=image, image_type="job", job=job)
                    images.append(ImageSerializer(image).data)
                # job.images = images

            return Response({
                "status": True,
                "data": JobSerializer(job).data,
            })

        return Response({
            "message": serializer.errors
        })
    except Exception as e:
        print('error: ', e)
        return Response({
            "status": False,
            "data": None,
            "message": "Please enter full of input field_id,author_id"

        })


@api_view(['PUT'])
def job_update_api(request, job_id):

    try:

        data = request.data
        images = list()
        location = list()

        job = Job.objects.get(id=job_id)

        if data.get('images'):
            for image in data.pop('images'):
                image = Image.objects.create(image=image)
                images.append(ImageSerializer(image).data)
            job.images = images

        if data.get('location'):
            location_str = data.get('location')
            location = json.loads(location_str)

        job.name = data.get('name') or job.name
        job.slug = slugify(job.name)
        job.suggestion_price = data.get(
            'suggestion_price') or job.suggestion_price
        job.field_id = data.get('field_id') or job.field_id
        job.descriptions = data.get('descriptions') or job.descriptions
        job.location = location or job.location
        job.save()
        serializer = JobSerializer(job)

        return Response({
            "status": True,
            "data": serializer.data
        })
    except Exception as e:
        print('error: ', e)
        return Response({
            "status": False,
            "data": None,
            "message": "Please enter full of input field_id,author_id"

        })


@api_view(['DELETE'])
def job_delete_api(self, job_id):

    try:
        job = Job.objects.get(id=job_id)
        job.delete()

        return Response({
            "status": True,
            "data": None,
            "message": "Delete successfully"
        })
    except Exception as e:

        return Response({
            "status": False,
            "data": None,
            "message": "Delete Failed"

        })


@api_view(['GET'])
def job_filter_api(request):

    try:
        province_code = request.query_params.get('province_code')
        district_code = request.query_params.get('district_code')
        subdistrict_code = request.query_params.get('subdistrict_code')
        field_id = request.query_params.get('field_id')

        paginator = JobPaginationCustom()
        paginator.page_size = 10

        if subdistrict_code and district_code and province_code:

            if field_id:
                jobs_filtered = Job.objects.filter(
                    location__province_code__contains=province_code,
                    location__district_code__contains=district_code,
                    location__subdistrict_code__contains=subdistrict_code,
                    status='published'
                ).filter(field_id=field_id).all()
            else:
                jobs_filtered = Job.objects.filter(
                    location__province_code__contains=province_code,
                    location__district_code__contains=district_code,
                    location__subdistrict_code__contains=subdistrict_code,
                    status='published'
                ).all()

        elif province_code and district_code:

            if field_id:
                jobs_filtered = Job.objects.filter(
                    location__province_code__contains=province_code,
                    location__district_code__contains=district_code,
                    status='published'
                ).filter(field_id=field_id).all()
            else:
                jobs_filtered = Job.objects.filter(
                    location__province_code__contains=province_code,
                    location__district_code__contains=district_code,
                    status='published'
                ).all()

        elif province_code:

            if field_id:
                jobs_filtered = Job.objects.filter(
                    location__province_code__contains=province_code,
                    status='published'
                ).filter(field_id=field_id).all()
            else:
                jobs_filtered = Job.objects.filter(
                    location__province_code__contains=province_code,
                    status='published'
                ).all()

        elif field_id:

            jobs_filtered = Job.objects.filter(
                field_id=field_id, status='published').all()

        else:

            jobs_filtered = None

        # check jobs_filtered
        if jobs_filtered is not None:
            context = paginator.paginate_queryset(jobs_filtered, request)
            serializer = JobSerializer(context, many=True)
            return Response(
                paginator.get_paginated_response(serializer.data)
            )
        else:
            return Response({
                "status": False,
                "data": None,
                "message": "Not found any data"
            })

    except Exception as e:
        print('error at: ', e)
        return Response({
            "status": False,
            "data": None,
            "message": "Filter Failed"
        })


@api_view(['GET'])
def job_search_api(request):

    try:

        search_word = request.query_params.get('query')

        search_vector = SearchVector('name', 'descriptions')
        search_query = SearchQuery(search_word)
        paginator = JobPaginationCustom()
        paginator.page_size = 10

        results = Job.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by('rank')

        context = paginator.paginate_queryset(results, request)
        serializer = JobSerializer(context, many=True)

        return Response(
            paginator.get_paginated_response(serializer.data)
        )
    except Exception as e:
        print('error at: ', e)
        return Response({
            "status": False,
            "data": None,
            "message": "Search Failed"
        })


# JobCollaborator API
@api_view(['POST'])
def jobcandidate_post_api(request):
    try:
        data = request.data
        jobcandidate = JobCandidate()
        serializer = JobCandidateSerializer(jobcandidate, data=data)

        if serializer.is_valid():
            print('data valid')
            jobcandidate.expected_price = data.get('expected_price')
            jobcandidate.descriptions = data.get('descriptions')
            jobcandidate.candidate_id = data.get('candidate_id')
            jobcandidate.job_id = data.get('job_id')

            jobcandidate.save()

            print('jobcandidate: ', JobCandidateSerializer(jobcandidate).data)

            return Response({
                "status": True,
                "data": JobCandidateSerializer(jobcandidate).data,
                "message": "Create job candidate successfully."
            })

        else:
            return Response({
                "status": True,
                "data": None,
                "message": serializer.errors
            })

    except Exception as e:
        print('error at: ', e)
        return Response({
            "status": False,
            "data": None,
            "message": "create failed"
        })


@api_view(['GET'])
def jobcandidate_get_api(request):
    jobcandidate = JobCandidate.objects.all()

    return Response({
        "status": True,
        "data": JobCandidateSerializer(jobcandidate, many=True).data
    })


# User or Author
@api_view(['GET'])
def user_jobs_api(request, user_id):

    try:

        job_status = request.query_params.get('job_status')

        paginator = JobPaginationCustom()
        paginator.page_size = 10

        user = User.objects.get(id=user_id)
        user_jobs = user.jobs.filter(status=job_status).order_by('created_at')

        context = paginator.paginate_queryset(user_jobs, request)
        serializer = JobSerializer(context, many=True)

        return Response(
            paginator.get_paginated_response(serializer.data)
        )

    except Exception as e:
        print('error at: ', e)
        return Response({
            "status": False,
            "data": None,
            "message": "Error"
        })


# Candidate
@api_view(['GET'])
def candidate_job_api(request, user_id):

    try:

        paginator = PaginationBaseCustom()

        apply_status = request.query_params.get('apply_status')

        candidate = User.objects.get(id=user_id)
        candidate_apply = candidate.usercandidate.filter(
            status=apply_status).order_by('created_at').all()

        context = paginator.paginate_queryset(candidate_apply, request)
        serializer = JobCandidateSerializer(context, many=True)

        return Response(
            paginator.get_paginated_response(serializer.data)
        )

    except Exception as e:
        print('error at: ', e)
        return Response({
            "status": False,
            "data": None,
            "message": "Error"
        })
