from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'service'

urlpatterns = [
    path('api/v1/category',views.category_list_api,name='category_list_api'),
    path('api/v1/fields',views.field_list_api,name='field_list_api'),
    path('api/v1/jobs',views.job_list_api,name='job_list_api'),
    path('api/v1/customer',views.user_signup,name='customer_signup'),
    path('api/v1/customer/<int:customer_id>',views.user_update,name='customer_update'),
    path('api/v1/customers',views.customer_list_api,name='customer_list'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

