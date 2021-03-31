from firebase_admin import messaging
from rest_framework.response import Response
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery

from .models import (
    Category,
    Job,
    Field,
    Image,
    JobCandidate,
    CandidateUser,
    Review,
    ServiceUser,
    Notification as NotificationModel
)
from django.utils.text import slugify
from .serializers import (
    CategorySerializer,
    FieldSerializer,
    JobSerializer,
    UserSingupSerializer,
    JobPaginationCustom,
    AuthorSerializer,
    ImageSerializer,
    JobCandidateSerializer,
    PaginationBaseCustom,
    CandidateUserSerializer,
    ReviewSerializer,
    ServiceUserSerializer,
    ServiceUserSigninSerializer,
    NotificationSerializer
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

from service.firebase_notification import Notification

from service.helper import Log, ErrorCode

from local_env.config import SERVER_PATH

import time

log = Log()


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


# User API
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):

    try:
        serializer = UserSingupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.create(validated_data=request.data)
            user.save()
            return Response({
                "status": True,
                "user": ServiceUserSerializer(user).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            })

        message = 'Error: %s' % serializer.errors
        log.log_message(message)
        return Response({
            "status": False,
            "error_messages": serializer.errors
        })
    except Exception as e:
        message = f'Error: {e}'
        log.log_message(message)
        return Response({
            "status": False,
            "message": "Register failed %s" % message,
            "data": None
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):

    try:
        serializer = ServiceUserSigninSerializer(data=request.data)

        if serializer.is_valid():
            phonenumber = request.data.get('phonenumber')
            password = request.data.get('password')

            user = ServiceUser.objects.filter(
                phonenumber=phonenumber, status='published').first()

            if user is not None:

                if user.check_password(password) is True:

                    refresh = RefreshToken.for_user(user)

                    return Response({
                        "status": True,
                        "user": ServiceUserSerializer(user).data,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        # "candidate_info":candidate_info
                    })
                else:
                    return Response({
                        "status": False,
                        "user": None,
                        "message": "Please check password correctly!"
                    })
            else:
                return Response({
                    "status": False,
                    "user": None,
                    "message": "Please check phonenumber correctly!"
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
        message = f'Error: {error}'
        log.log_message(message)
        return Response({
            "status": False,
            "message": "Login failed %s" % message,
            "data": None
        })
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
            candidate_user.location = location
            candidate_user.save()
            candidate_user.category.set(categories)
            candidate_user.fields.set(fields)

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
        candidate_user.descriptions = data.get('descriptions')

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
@permission_classes([AllowAny])
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

    serializer = FieldSerializer(field)
    return Response(serializer.data)


@api_view(['GET'])
def customer_list_api(request):
    users = ServiceUser.objects.all()
    serializer = ServiceUserSerializer(users, many=True)

    return Response(serializer.data)


# Job API

# Return job list exclude created by author
@api_view(['GET'])
def job_list_api(request):

    page = request.query_params.get('page')
    page_limit = request.query_params.get('limit')
    category_slug = request.query_params.get('category_slug')
    field_slug = request.query_params.get('field_slug')
    user_id = request.query_params.get('user_id')

    paginator = JobPaginationCustom()
    paginator.page_size = 10

    if page_limit is not None:
        paginator.page_size = int(page_limit)

    if category_slug is not None:
        try:
            cat = Category.objects.get(slug=category_slug)
            fields = cat.fields.all()
            jobs = Job.objects.filter(
                field__in=fields, status='published').exclude(author_id=user_id).order_by('-created_at').all()
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
                field=field, status='published').exclude(author_id=user_id).order_by('-created_at').all()
            context = paginator.paginate_queryset(jobs, request)
            serializer = JobSerializer(context, many=True)

            return Response(paginator.get_paginated_response(serializer.data))

        except Field.DoesNotExist:
            return Response({
                "status": False,
                "message": "Field is not exists"
            })

    query_set = Job.objects.filter(status='published').exclude(
        author_id=user_id).order_by('-created_at')
    context = paginator.paginate_queryset(query_set, request)
    serializer = JobSerializer(context, many=True)

    return Response(
        paginator.get_paginated_response(serializer.data)
    )


@api_view(['GET'])
def job_detail_api(request, job_id=None):

    if job_id is not None:
        try:
            job = Job.objects.get(id=job_id)
            serializer = JobSerializer(job)
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

                    # print(image.get_absolute_url())
                    images.append(image)
                # job.images = images

            # image_url = images[0].get_absolute_url()
            image_url = "https://iso.500px.com/wp-content/uploads/2016/11/stock-photo-159533631-1500x1000.jpg"
            notification = Notification(
                title=job.name, body=job.descriptions, image=image_url)
            notification.send_topic_notification('jobpost')

            return Response({
                "status": True,
                "data": JobSerializer(job).data,
            })

        return Response({
            "message": serializer.errors
        })
    except Exception as e:
        print('error: ', e)
        log.log_message(e)
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
        message = f'Error: {e}'
        log.log_message(message)
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
        message = f'Error: {e}'
        log.log_message(message)
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
        message = f'Error: {e}'
        log.log_message(message)
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
        message = f'Error: {e}'
        log.log_message(message)
        return Response({
            "status": False,
            "data": None,
            "message": "Search Failed"
        })


# JobCollaborator API
@api_view(['POST'])
def apply_job_position(request, user_id):

    try:

        data = request.data

        jobcandidate = JobCandidate()
        serializer = JobCandidateSerializer(jobcandidate, data=data)

        if serializer.is_valid():

            candidate_id = data.get('candidate_id')
            user = CandidateUser.objects.filter(user_id=candidate_id).first()
            print(user)
            if user is None:
                return Response({
                    "status": False,
                    "data": None,
                    "message": "User is not registered candidate",
                    "code": ErrorCode.CANDIDATE_NOT_REGISTER
                })

            is_applied = JobCandidate.objects.filter(job_id=data.get(
                'job_id'), candidate_id=data.get('candidate_id')).all()

            if is_applied.count() > 0:
                return Response({
                    "status": False,
                    "data": None,
                    "message": "Candidate was apply this job",
                    "code": ErrorCode.CANDIDATE_EXIST

                })

            # print('is applied: ',is_applied)

            jobcandidate.expected_price = data.get('expected_price')
            jobcandidate.descriptions = data.get('descriptions')
            jobcandidate.candidate_id = data.get('candidate_id')
            jobcandidate.job_id = data.get('job_id')

            jobcandidate.save()

            return Response({
                "status": True,
                "data": JobCandidateSerializer(jobcandidate).data,
                "message": "Apply job position successfully.",
                "code": ErrorCode.SUCCESS
            })

        else:
            return Response({
                "status": False,
                "data": None,
                "message": serializer.errors
            })

    except Exception as e:
        print('error at: ', e)
        message = f'Error: {e}'
        log.log_message(message)
        return Response({
            "status": False,
            "data": None,
            "message": "create failed",
            "code": ErrorCode.UNDEFINED
        })


# User or Author
@api_view(['GET'])
def user_jobs_api(request, user_id):

    try:

        job_status = request.query_params.get('job_status')

        paginator = JobPaginationCustom()
        paginator.page_size = 10
        user = ServiceUser.objects.get(id=user_id)

        if job_status == "approved":

            user_approved_jobs = JobCandidate.objects.filter(
                job__status="approved", job__author_id=user_id).order_by('-updated_at').all()
            context = paginator.paginate_queryset(user_approved_jobs, request)
            serializer = JobCandidateSerializer(context, many=True)

        elif job_status == "confirmed":

            user_confirmed_jobs = JobCandidate.objects.filter(
                job__status="confirmed", job__author_id=user_id).order_by('-updated_at').all()
            context = paginator.paginate_queryset(user_confirmed_jobs, request)
            serializer = JobCandidateSerializer(context, many=True)

        else:

            user_jobs = user.jobs.filter(
                status="published").order_by('-created_at').all()
            context = paginator.paginate_queryset(user_jobs, request)
            serializer = JobSerializer(context, many=True)

        return Response(
            paginator.get_paginated_response(
                serializer.data, message="Get job created by user successfully", code=ErrorCode.GET_SUCCESS)
        )

    except Exception as e:
        print('error at: ', e)
        message = f'Error: {e}'
        print(message)
        log.log_message(message)
        return Response({
            "status": False,
            "data": None,
            "message": "Error: %s " % e,
            "code": ErrorCode.UNDEFINED
        })


@api_view(['GET'])
def get_user_detail(request, user_id):
    try:
        user = ServiceUser.objects.get(id=user_id)
        user_serializer = ServiceUserSerializer(user).data

        return Response({
            "status": True,
            "message": "Get user detail successfully",
            "data": user_serializer,
            "code": ErrorCode.GET_SUCCESS
        })

    except Exception as e:
        message = f'Error: {e}'
        print(message)
        log.log_message(message)
        return Response({
            "status": False,
            "message": "Get user detail failed",
            "data": None,
            "code": ErrorCode.UNDEFINED
        })


# User select or cancel candidate by change status
@api_view(['PUT'])
def modify_job_candidate(request, user_id):
    try:

        data = request.data
        jobcandidate_id = data.get('jobcandidate_id')
        jobcandidate_status = data.get('status')

        status_validation = jobcandidate_status in JobCandidate.STATUS_LIST

        if status_validation and jobcandidate_id is not None:

            job_candidate = JobCandidate.objects.get(id=jobcandidate_id)
            job_candidate.status = jobcandidate_status

            if jobcandidate_status == "approved":
                job_candidate.job.status = jobcandidate_status

            elif jobcandidate_status == "confirmed":
                job_candidate.confirmed_price = data.get('confirmed_price')
                job_candidate.job.status = jobcandidate_status

                try:
                    review = Review()
                    review.review_level = data.get('review_level')
                    review.review_content = data.get('review_content')
                    review.job_candidate = job_candidate
                    review.save()
                except Exception as e:
                    review = Review.objects.get(job_candidate=job_candidate)
                    review.review_level = data.get('review_level')
                    review.review_content = data.get('review_content')
                    review.save()

            else:
                job_candidate.job.status = "published"

            job_candidate.job.save()
            job_candidate.save()

            serializer = JobCandidateSerializer(job_candidate).data
            
            return Response({
                "status": True,
                "data": serializer,
                "message": "Modified cuccessfully",
                "code": ErrorCode.POST_SUCCESS
            })

        else:
            return Response({
                "status": False,
                "data": None,
                "message": "Errpr: Please check jobcandidate_status and jobcandidate_id",
                "code": ErrorCode.UNDEFINED

            })

    except Exception as e:
        message = f'Error: {e}'
        print(message)
        log.log_message(message)
        return Response({
            "status": False,
            "data": None,
            "message": message,
            "code": ErrorCode.UNDEFINED
        })


# User search candidate
@api_view(['GET'])
def search_candidate_api(request, user_id):

    try:
        page = request.query_params.get('page')
        page_limit = request.query_params.get('limit')

        paginator = PaginationBaseCustom()
        paginator.page_size = 10

        if page_limit is not None:
            paginator.page_size = int(page_limit)

        query = request.query_params.get('query')

        search_vector = SearchVector(
            'candidate_user__descriptions', 'candidate_user__fields__name')
        search_query = SearchQuery(query)

        candidate = ServiceUser.objects.annotate(
            search=search_vector,
        ).filter(search=search_query).distinct('id')
        context = paginator.paginate_queryset(candidate, request)
        serializer = ServiceUserSerializer(context, many=True)

        return Response(
            paginator.get_paginated_response(
                serializer.data, message="search candidate successfully", code=ErrorCode.GET_SUCCESS)
        )

    except Exception as e:
        message = f'Error: {e}'
        log.log_message(message)
        return Response({
            "status": False,
            "data": None,
            "message": message,
            "code": ErrorCode.UNDEFINED
        })


@api_view(['GET'])
def get_candidate_job_api(request, user_id):

    try:
        page = request.query_params.get('page')
        page_limit = request.query_params.get('limit')

        paginator = PaginationBaseCustom()
        paginator.page_size = 10

        if page_limit is not None:
            paginator.page_size = int(page_limit)

        apply_status = request.query_params.get('apply_status')

        status_validation = apply_status in JobCandidate.STATUS_LIST

        if status_validation and user_id:
            candidate = ServiceUser.objects.get(id=user_id)
            candidate_apply = candidate.usercandidate.filter(
                status=apply_status).order_by('created_at').all()

            context = paginator.paginate_queryset(candidate_apply, request)
            serializer = JobCandidateSerializer(context, many=True)

            return Response(
                paginator.get_paginated_response(
                    serializer.data, message="Get candidate applied jobs successfully ", code=ErrorCode.GET_SUCCESS)
            )
        else:
            return Response({
                "status": False,
                "data": None,
                "message": "Please check user_id and apply_status",
                "code": ErrorCode.VALIDATION
            })

    except Exception as e:
        message = f'Error: {e}'
        log.log_message(message)
        return Response({
            "status": False,
            "data": None,
            "message": message,
            "code": ErrorCode.UNDEFINED
        })


@api_view(['GET'])
def get_candidate_review_api(request, user_id):
    try:
        page = request.query_params.get('page')
        page_limit = request.query_params.get('limit')
        paginator = PaginationBaseCustom()
        paginator.page_size = 10

        if page_limit is not None:
            paginator.page_size = int(page_limit)

        reviews = Review.objects.filter(
            job_candidate__candidate_id=user_id).order_by('-updated_at').all()

        context = paginator.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(context, many=True)

        return Response(
            paginator.get_paginated_response(
                serializer.data, message="Get candidate review successfully", code=ErrorCode.GET_SUCCESS)
        )

    except Exception as e:
        message = f'Error: {e}'
        log.log_message(message)
        return Response({
            "status": False,
            "data": None,
            "message": message,
            "code": ErrorCode.UNDEFINED
        })


@api_view(['GET'])
def get_candidate_images(request, user_id):
    try:
        page = request.query_params.get('page')
        page_limit = request.query_params.get('limit')
        paginator = PaginationBaseCustom()
        paginator.page_size = 10

        if page_limit is not None:
            paginator.page_size = int(page_limit)

        images = Image.objects.filter(
            status='published', candidate_user=user_id, image_type="job"
        ).all()

        context = paginator.paginate_queryset(images, request)
        serializer = ImageSerializer(context, many=True)

        return Response(
            paginator.get_paginated_response(
                serializer.data, message="Get candidate job image successfully", code=ErrorCode.GET_SUCCESS)
        )

    except Exception as e:
        message = f'Error: {e}'
        log.log_message(message)
        return Response({
            "status": False,
            "data": None,
            "message": message,
            "code": ErrorCode.UNDEFINED
        })


@api_view(['GET'])
def get_candidate_notifications(request, user_id):
    try:

        page = request.query_params.get('page')
        page_limit = request.query_params.get('limit')
        paginator = PaginationBaseCustom()
        paginator.page_size = 10
        if page_limit is not None:
            paginator.page_size = int(page_limit)

        candidate_notification = NotificationModel.objects.filter(
            user_id=user_id).all()

        context = paginator.paginate_queryset(candidate_notification, request)
        serializer = NotificationSerializer(context, many=True)

        return Response(
            paginator.get_paginated_response(
                serializer.data, message="Get candidate notifications successfully", code=ErrorCode.GET_SUCCESS)
        )

    except Exception as e:
        message = f'Error: {e}'
        log.log_message(message)
        return Response({
            "status": False,
            "data": None,
            "message": message,
            "code": ErrorCode.UNDEFINED
        })


@api_view(['PUT'])
def update_candidate_notification(request, user_id, notification_id):
    try:

        candidate_notification = NotificationModel.objects.get(id=notification_id,user_id=user_id)
        candidate_notification.status = 'read'
        candidate_notification.save()

        serializer = NotificationSerializer(candidate_notification).data

        return Response({
            "status": True,
            "data": serializer,
            "message": "update candidate notification status cuccessfully",
            "code": ErrorCode.POST_SUCCESS
        })

    except Exception as e:
        message = f'Error: {e}'
        log.log_message(message)
        return Response({
            "status": False,
            "data": None,
            "message": message,
            "code": ErrorCode.UNDEFINED
        })
