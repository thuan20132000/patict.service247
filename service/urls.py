from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static
from .api import (
    job_list_api,
    category_list_api,
    field_list_api,
    customer_list_api,
    category_detail_api,
    job_detail_api,
    job_post_api,
    job_update_api,
    job_delete_api,
    job_filter_api,
    job_search_api
)

app_name = 'service'

urlpatterns = [
    path('api/v1/category',category_list_api,name='category_list_api'),
    path('api/v1/category/<slug:category_slug>',category_detail_api,name='category_detail_api'),
    path('api/v1/fields',field_list_api,name='field_list_api'),
    path('api/v1/jobs',job_list_api,name='job_list_api'),
    path('api/v1/jobs/<int:job_id>',job_detail_api,name='job_detail_api'),
    path('api/v1/job',job_post_api,name='job_post_api'),
    path('api/v1/job/<int:job_id>',job_update_api,name='job_update_api'),
    path('api/v1/job/<int:job_id>/delete',job_delete_api,name='job_delete_api'),
    path('api/v1/job/filter',job_filter_api,name='job_filter_api'),
    path('api/v1/job/search',job_search_api,name='job_search_api'),
    path('api/v1/customers',customer_list_api,name='customer_list_api'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

