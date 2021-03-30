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
    Notification
)


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Field)
class AdminField(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name",)}


@admin.register(Job)
class AdminJob(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name',)}
    list_display = ('name', 'descriptions', 'location', 'get_author','created_at')

    def get_author(self, obj):
        if obj.name:
            return mark_safe('<a href="%s">%s</a>' % (obj.author.get_absolute_url(),obj.author.username))
        else:
            return 'Not Available'


@admin.register(JobCandidate)
class AdminJobCandidate(admin.ModelAdmin):
    pass


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
                    'status', 'gender', 'created_at')

    list_filter = ('gender','status','candidate_user__fields')



@admin.register(Notification)
class AdminNotification(admin.ModelAdmin):
    list_display = ('title','content','user_id','job_id')