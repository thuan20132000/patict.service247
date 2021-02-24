from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'service'

urlpatterns = [
    path('api/v1/category',views.category_list_api,name='category_list_api'),
    path('api/v1/fields',views.field_list_api,name='field_list_api'),
    path('api/v1/jobs',views.job_list_api,name='job_list_api'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

