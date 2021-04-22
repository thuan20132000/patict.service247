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
    job_search_api,
    apply_job_position,
    user_jobs_api,
    field_detail_api,
    get_candidate_job_api,
    register_candidate_api,
    update_candidate_api,
    modify_job_candidate,
    get_candidate_review_api,
    search_candidate_api,
    get_candidate_images,
    get_user_detail,
    get_user_notifications,
    update_user_notification,
    update_user_notification_token,
    get_jobcandidate_detail_trackking,
    get_user_notification_configuration,
    update_user_notification_configuration,
    get_candidate_services,
    create_candidate_service,
    delete_candidate_service,
    book_services,
    get_candidate_booking,
    get_candidate_booking_detail,
    update_booking,
    create_confirm_booking_review,

    
)

app_name = 'service'

urlpatterns = [
    path('api/v1/category',category_list_api,name='category_list_api'),
    path('api/v1/category/<slug:category_slug>',category_detail_api,name='category_detail_api'),
    path('api/v1/fields',field_list_api,name='field_list_api'),
    path('api/v1/fields/<int:field_id>',field_detail_api,name='field_detail_api'),
    
    path('api/v1/jobs',job_list_api,name='job_list_api'),
    path('api/v1/jobs/<int:job_id>',job_detail_api,name='job_detail_api'),
    path('api/v1/job',job_post_api,name='job_post_api'),
    path('api/v1/job/<int:job_id>',job_update_api,name='job_update_api'),
    path('api/v1/job/<int:job_id>/delete',job_delete_api,name='job_delete_api'),
    path('api/v1/job/filter',job_filter_api,name='job_filter_api'),
    path('api/v1/job/search',job_search_api,name='job_search_api'),
    path('api/v1/user/<int:user_id>/apply-job',apply_job_position,name='apply_job_api'),
    path('api/v1/customers',customer_list_api,name='customer_list_api'),

    # Get all jobs that created by user with status [published,pending,draft,confirmed]
    path('api/v1/user/<int:user_id>/jobs',user_jobs_api,name='user_jobs_api'),
    
    # user
    path('api/v1/user/<int:user_id>/register-candidate',register_candidate_api,name='register_candidate_api'),
    path('api/v1/user/<int:user_id>/update-candidate',update_candidate_api,name='update_candidate_api'),
    # user select or cancel candidate
    path('api/v1/user/<int:user_id>/jobcandidate',modify_job_candidate,name='modify_jobcandidate_api'),
    # user detail
    path('api/v1/user/<int:user_id>/detail',get_user_detail,name="get_user_detail"),
    #user search
    path('api/v1/user/<int:user_id>/search-candidate',search_candidate_api,name='search_candidate_api'),
    # update user notification token
    path('api/v1/user/<int:user_id>/notification-token',update_user_notification_token,name='update_user_notificatin_api'),
    # get user notification configurations
    path('api/v1/user/<int:user_id>/notification-configuration',get_user_notification_configuration,name='get_user_notification_configuration'),
    path('api/v1/user/<int:user_id>/notification-configuration/update',update_user_notification_configuration,name='update_user_notification_configuration'),

    path('api/v1/user/<int:user_id>/services/book',book_services,name="book_services"),

    # Get all jobs that candidates has been applied by job status
    path('api/v1/candidate/<int:user_id>/jobs',get_candidate_job_api,name='candidate_jobs_api'),
    path('api/v1/candidate/<int:user_id>/reviews',get_candidate_review_api,name='candidate_reviews_api'),

    # notification
    path('api/v1/user/<int:user_id>/notifications',get_user_notifications,name="get_user_notifications"),
    path('api/v1/user/<int:user_id>/notification/<int:notification_id>',update_user_notification,name="update_user_notification"),
    # candidate
    path('api/v1/candidate/<int:user_id>/images',get_candidate_images,name="get_candidate_image"),
    path('api/v1/candidate/<int:user_id>/jobcandidate/<int:jobcandidate_id>/detail',get_jobcandidate_detail_trackking,name="get_jobcandidate_detail"),
    path('api/v1/candidate/<int:user_id>/services',get_candidate_services,name="get_candidate_services"),
    path('api/v1/candidate/<int:user_id>/service',create_candidate_service,name="create_candidate_service"),
    path('api/v1/candidate/<int:user_id>/service/<int:service_id>',delete_candidate_service,name='delete_candidate_service'),
    path('api/v1/candidate/<int:user_id>/booking',get_candidate_booking,name="get_candidate_booking"),
    path('api/v1/candidate/<int:user_id>/booking/<int:order_id>',get_candidate_booking_detail,name="get_candidate_booking_detail"),



    #order_booking
    path('api/v1/user/<int:user_id>/booking/<int:booking_id>/update',update_booking,name="update_booking"),
    path('api/v1/user/<int:user_id>/booking/<int:booking_id>/confirm',create_confirm_booking_review,name="create_confirm_booking_review"),



] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

