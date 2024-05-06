
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # Add path to create a new post.
    path("new_post", views.new_post, name="new_post"),
    # Add path to user's profile page.
    path("profile/<int:id>", views.profile, name="profile"),
    # Add path to follow a user.
    path("follow/<int:user>", views.follow, name="follow"),
    # Add path to unfollow a user.
    path("unfollow/<int:user>", views.unfollow, name="unfollow"),
    # Add path to following page.
    path("following/<int:id>", views.following, name="following"),
    # Add path to edit a post.
    path("edit/<int:post_id>", views.edit, name="edit"),
    # Add path to like a post.
    path("like/<int:post_id>", views.like, name="like")
]
