from . import models
from django.contrib import admin
# Register your models here.
# admin.site.register(models.Category)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['name']}
    list_display = ['name','slug']

admin.site.register(models.Categories,CategoriesAdmin)
