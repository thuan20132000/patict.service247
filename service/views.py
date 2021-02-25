from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from .models import Category,Field,Job,User

