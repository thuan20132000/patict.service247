from django.contrib import admin
from django.utils.html import mark_safe
# Register your models here.
from .models import (
    Category,
    Field,
    JobCandidate,
    Job,
    CandidateUser,
    ServiceUser,
    Notification,
    UserNotificationConfiguration,
    CandidateService,
    ServiceBooking
)

from django.contrib.contenttypes.admin import GenericTabularInline, InlineModelAdmin
from django.forms.models import BaseInlineFormSet
from django.contrib.admin import SimpleListFilter
from django_json_widget.widgets import JSONEditorWidget
from django.db import models


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'status',)
    list_editable = ('status',)


@admin.register(Field)
class AdminField(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'status',)

    list_editable = ('status',)


class JSONFieldFilter(SimpleListFilter):
    """
    """

    def __init__(self, *args, **kwargs):

        super(JSONFieldFilter, self).__init__(*args, **kwargs)

        assert hasattr(self, 'title'), (
            'Class {} missing "title" attribute'.format(
                self.__class__.__name__)
        )
        assert hasattr(self, 'parameter_name'), (
            'Class {} missing "parameter_name" attribute'.format(
                self.__class__.__name__)
        )
        assert hasattr(self, 'json_field_name'), (
            'Class {} missing "json_field_name" attribute'.format(
                self.__class__.__name__)
        )
        assert hasattr(self, 'json_field_property_name'), (
            'Class {} missing "json_field_property_name" attribute'.format(
                self.__class__.__name__)
        )

    def lookups(self, request, model_admin):
        """
        # Improvemnt needed: if the size of jsonfield is large and there are lakhs of row
        """
        if '__' in self.json_field_property_name:  # NOTE: this will cover only one nested level
            keys = self.json_field_property_name.split('__')
            field_value_set = set(
                data[keys[0]][keys[1]] for data in model_admin.model.objects.values_list(self.json_field_name, flat=True)
            )
        else:
            field_value_set = set(
                data[self.json_field_property_name] for data in model_admin.model.objects.values_list(self.json_field_name, flat=True)
            )
        return [(v, v) for v in field_value_set]

    def queryset(self, request, queryset):
        if self.value():
            json_field_query = {"{}__{}".format(
                self.json_field_name, self.json_field_property_name): self.value()}
            return queryset.filter(**json_field_query)
        else:
            return queryset


class ProvinceFilter(JSONFieldFilter):
    json_field_name = 'location'  # Name of the column in the model
    json_field_property_name = 'province'  # property/field name in json data
    title = 'Name'  # A label for this filter for admin sidebar
    # Parameter for the filter that will be used in the URL query
    parameter_name = 'js_province'


class JobCandidateInline(admin.TabularInline):
    model = JobCandidate
    extra = 1
    fields = ('candidate', 'expected_price', 'status')
    readonly_fields = ('candidate', 'expected_price')


@admin.register(Job)
class AdminJob(admin.ModelAdmin):

    formfield_overrides = {
        # models.JSONField: {'widget': JSONEditorWidget},  # if django < 3.1
        models.JSONField: {'widget': JSONEditorWidget},
    }
    fields = ('name', 'status', 'author', 'descriptions', 'created_at', 'location','slug',)
    readonly_fields = ['created_at',]
    prepopulated_fields = {"slug": ('name',)}
    list_display = ('name', 'candidate_number', 'status', 'author', 'descriptions',
                    'get_author', 'created_at','province')
    list_filter = ['status', ProvinceFilter]
    date_hierarchy = 'created_at'
    
    inlines = [
        JobCandidateInline
    ]

    def candidate_number(self, obj):
        if obj.jobcandidate:
            return obj.jobcandidate.all().count()
        else:
            return 'None'

    def get_author(self, obj):
        if obj.name:
            return mark_safe('<a href="%s">%s</a>' % (obj.author.get_absolute_url(), obj.author.username))
        else:
            return 'Not Available'

    def province(self, obj):
        if obj.location:
            return '%s - %s'%(obj.location.get('district'),obj.location.get('province'))
        else:
            return 'None'


@admin.register(JobCandidate)
class AdminJobCandidate(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'get_field',
                    'expected_price', 'descriptions', 'status', 'updated_at')
    list_filter = ('status', 'job__field', 'job__field__category')
    list_editable = ('status',)

    def get_field(self, obj):

        if obj.job:
            return obj.job.field
        else:
            return 'Not available'


@admin.register(CandidateUser)
class AdminCandidateUser(admin.ModelAdmin):
    pass
# ServiceUSer


class UserJob(admin.AdminSite):
    model = Job
    extra = 2


@admin.register(ServiceUser)
class AdminServiceUser(admin.ModelAdmin):
    list_display = ('username', 'phonenumber',
                    'status', 'gender', 'created_at','notification_token')

    list_filter = ('gender', 'status', 'candidate_user__fields')


@admin.register(Notification)
class AdminNotification(admin.ModelAdmin):
    list_display = ('title', 'content', 'job_id',
                    'status', 'get_user_url', 'created_at')
    list_per_page = 30

    def get_user_url(self, obj):
        if obj.user_id:
            return mark_safe('<a href="%s">%s</a>' % (obj.get_user_url(), obj.user.username))
        else:
            return 'Not Available'

    def get_job(self, obj):
        if obj.job:
            return mark_safe('<a href="%s">%s</a>' % (obj.job.get_absolute_url(), obj.job.name))
        else:
            return 'Not Available'


@admin.register(UserNotificationConfiguration)
class AdminUserNotificationConfiguration(admin.ModelAdmin):
    list_display = ('post_job_notification', 'apply_job_notification',
                    'user_job_notification', 'user_message_notification', 'user')

@admin.register(CandidateService)
class AdminCandidateService(admin.ModelAdmin):
    list_display = ['name','price','field','candidate','status']
    

@admin.register(ServiceBooking)
class AdminServiceBooking(admin.ModelAdmin):

    list_display = ['candidate','user','total_price','payment','created_at']