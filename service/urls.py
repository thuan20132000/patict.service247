from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static
from .api import job_list_api,category_list_api,field_list_api,customer_list_api

app_name = 'service'

urlpatterns = [
    path('api/v1/category',category_list_api,name='category_list_api'),
    path('api/v1/fields',field_list_api,name='field_list_api'),
    path('api/v1/jobs',job_list_api,name='job_list_api'),
    path('api/v1/customers',customer_list_api,name='customer_list_api'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

