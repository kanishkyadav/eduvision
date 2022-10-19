from django.contrib import admin
from .models import Post, Category, ContactUs

admin.site.register(Post)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('tutorial_name', 'discription', 'slug')


admin.site.register(ContactUs)
