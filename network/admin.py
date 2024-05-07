from django.contrib import admin

# Register your models here.
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
# Also, register the model in the app’s admin.py:

from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Follow, Like

# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#modeladmin-objects
class UserAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    pass

class FollowAdmin(admin.ModelAdmin):
    pass

class LikeAdmin(admin.ModelAdmin):
    pass


# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
# Also, register the (User) model in the app’s admin.py.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Like, LikeAdmin)