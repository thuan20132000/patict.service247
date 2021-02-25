from django.contrib import admin

# Register your models here.
from .models import Category,Field,JobCollaborator,Job



@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Field)
class AdminField(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name",)}



@admin.register(Job)
class AdminJob(admin.ModelAdmin):
    prepopulated_fields = {"slug":('name',)}



