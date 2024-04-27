
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
    path("profile/<int:id>", views.profile, name="profile")
]
