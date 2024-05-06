from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    signed_in = models.BooleanField(default=False)


class Post(models.Model):
    title = models.CharField(max_length=100)

    post = models.TextField()

    # https://docs.djangoproject.com/en/5.0/ref/models/fields/#integerfield
    likes = models.IntegerField() # Begins at 0

    # https://docs.djangoproject.com/en/5.0/ref/models/fields/#django.db.models.DateField
    # auto_now - "Automatically set the field to now every time the object is saved.  Useful for “last-modified” timestamps. Note that the current date is always used; it’s not just a default value that you can override."
    # auto_now_add - "Automatically set the field to now when the object is first created. Useful for creation of timestamps. Note that the current date is always used; it’s not just a default value that you can override. So even if you set a value for this field when creating the object, it will be ignored. If you want to be able to modify this field, set the following instead of auto_now_add=True."
    created = models.DateTimeField(auto_now=False,  auto_now_add=True) 

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return f"{self.title} / {self.author}"


# https://stackoverflow.com/questions/62304990/how-to-implement-a-follow-sistem-on-django-project
# https://stackoverflow.com/questions/58794639/how-to-make-follower-following-system-with-django-model
class Follow(models.Model):
    user_follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f"{self.user_follows}"
        # return f"{self.following_user} is following {self.user_follows}"


class Like(models.Model):
    like = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')