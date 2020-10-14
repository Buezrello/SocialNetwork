from django.contrib import admin

from .models import User, Post, Like

admin.site.register(User)
admin.site.register(Like)


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_text', 'created')


admin.site.register(Post, PostAdmin)
