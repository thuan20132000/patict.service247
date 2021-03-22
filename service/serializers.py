from rest_framework import serializers
from .models import (
    Category,
    Field,
    Job,
    User,
    Image,
    JobCandidate,
    CandidateUser,
    Review
)
from django.conf import settings
from rest_framework.pagination import PageNumberPagination, BasePagination

from django.utils.text import slugify
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Avg, Count


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        depth = 1
        fields = '__all__'


class UserSingupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],

        )
        user.set_password(validated_data['password'])
        return user


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField()
    password = serializers.CharField()
    candidate_info = serializers.SerializerMethodField('get_candidate_info')

    class Meta:
        model = User
        depth = 2
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

    def get_candidate_info(self, obj):
        if hasattr(obj, 'candidate_user'):
            return CandidateUserSerializer(obj.candidate_user).data
        return None


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        depth = 1
        fields = ['id', 'name', 'image', 'status', 'slug', 'fields']


class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field
        fields = ['id', 'name', 'image', 'status', 'slug']


class JobSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    suggestion_price = serializers.DecimalField(
        required=True, decimal_places=2, max_digits=18)
    # field_id = serializers.IntegerField(required=True)
    slug = serializers.SlugField(required=False)

    candidates = serializers.SerializerMethodField('get_candidates')
    images = serializers.SerializerMethodField('get_job_images')

    class Meta:
        model = Job
        depth = 1
        fields = '__all__'

    def create(self, validated_data):
        job = Job()
        job.name = validated_data['name']
        job.slug = validated_data['slug']
        job.suggestion_price = validated_data['suggestion_price']
        job.author = validated_data['author']
        job.field = validated_data['field']
        return job

    def create_new_job(self, validated_data):
        # print(validated_data)

        job = Job()
        job.name = validated_data.get('name')
        job.slug = slugify(validated_data.get('name'))
        job.suggestion_price = validated_data['suggestion_price']
        job.author_id = validated_data['author_id']
        job.field_id = validated_data['field_id']
        images = validated_data.pop('images')
        for image in images:
            image = Image.objects.create(image_url=image, job_id=job.id)
            print('image: ', image)

        return job

    def get_candidates(self, obj):
        return JobCandidateSerializer(obj.jobcandidate.all(), many=True).data

    def get_job_images(self, obj):
        return ImageSerializer(obj.jobs.filter(status='published').all(), many=True).data


class JobCandidateSerializer(serializers.ModelSerializer):

    confirmed_price = serializers.DecimalField(
        max_digits=18, decimal_places=2, required=False)
    reviews = serializers.SerializerMethodField('get_review')

    class Meta:
        model = JobCandidate
        depth = 1
        fields = '__all__'

    def get_review(self, obj):
        return ReviewSerializer(obj.reviews.filter(status="published").all(), many=True).data


class CandidateUserSerializer(serializers.ModelSerializer):

    images = serializers.SerializerMethodField('get_candidate_images')
    reviews = serializers.SerializerMethodField('get_candidate_reviews')
    review_overall = serializers.SerializerMethodField('get_review_overall')

    class Meta:
        model = CandidateUser
        depth = 1
        fields = '__all__'

    def get_candidate_images(self, obj):
        return ImageSerializer(obj.candidate_user.filter(status='published').all()[:3], many=True).data

    def get_candidate_reviews(self, obj):
        reviews = Review.objects.filter(
            job_candidate__candidate_id=obj.user_id)[:4]
        return ReviewSerializer(reviews.all(), many=True).data

    def get_review_overall(self, obj):
        reviews_overall = Review.objects.filter(job_candidate__candidate_id=obj.user_id).aggregate(
            review_level_avg=Avg('review_level'), review_count=Count('id'))
        # print('reviews: ',reviews)
        return reviews_overall


class JobPaginationCustom(PageNumberPagination):

    def get_paginated_response(self, data):
        return {
            "status": True,
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'limit': self.page_size,
            'data': data,
        }


class PaginationBaseCustom(PageNumberPagination):

    def get_paginated_response(self, data):
        return {
            "status": True,
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "limit": self.page_size,
            "data": data
        }
