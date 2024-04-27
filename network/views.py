from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post

from .forms import CreatePostForm


def index(request):

    """
    All Posts: The “All Posts” link in the navigation bar should take the user to a page where they can see all posts from all users, with the most recent posts first.
    https://docs.djangoproject.com/en/5.0/ref/models/querysets/#order-by - The negative sign in front of "-created" indicates descending order.
    """
    all_posts = Post.objects.all().order_by('-created')

    # Include the “New Post” form before “All Posts” on index.html. 
    form = CreatePostForm()

    context = {
        "all_posts": all_posts,
        "form": form
    }

    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

"""
New Post: Authenticated users may write a new text-based post. The number of “likes” the post has will be 0 to start.   
""" 

def new_post(request):
    # POST request
    if request.method == 'POST':
        newPost = CreatePostForm(request.POST)

        user_name = request.user

        title = newPost['title'].value()
        post = newPost['post'].value()

        newPost = Post(            
            title=title,
            post=post,
            likes=0,
            author=user_name
        )

        newPost.save()

        return HttpResponseRedirect(reverse('index'))
