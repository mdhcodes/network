from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follow

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
            # If a user is signed in, signed_in == true.
            user_id = request.user.id
            log_in_user = User.objects.get(pk=user_id)
            log_in_user.signed_in = True
            log_in_user.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    # If a user is not signed in, signed_in == false.
    user_id = request.user.id
    log_out_user = User.objects.get(pk=user_id)
    log_out_user.signed_in = False
    log_out_user.save()

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
    

    """
    Profile Page: Display the number of followers the user has, as well as the number of people that the user follows.
    Display all of the posts for that user, in reverse chronological order. 
    For any other user who is signed in, this page should also display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. 
    (Note that this only applies to any “other” user: a user should not be able to follow themselves.)
    """

def profile(request, id):

    user_name = request.user
    
    # Get number of followers the user has and the number of people the user follows.
    # https://stackoverflow.com/questions/58794639/how-to-make-follower-following-system-with-django-model
    user = User.objects.get(id=id)
    all_followers = len(user.followers.all())
    # print('Followers:', all_followers)
    all_following = len(user.following.all())
    # print('Following:', all_following)

    # Display all of the posts for that user, in reverse chronological order.
    all_posts = user.user.all().order_by('-created')
    # print('All Posts:', all_posts)

    # Get all users who are signed in.
    # If a user is signed in, signed_in == true. This list should not include the user on this page.
    # https://stackoverflow.com/questions/2354284/django-queries-how-to-filter-objects-to-exclude-id-which-is-in-a-list
    # https://docs.djangoproject.com/en/5.0/topics/db/queries/#retrieving-specific-objects-with-filters
    # exclude(**kwargs) - Returns a new QuerySet containing objects that do not match the given lookup parameters.
    signed_in_users = User.objects.filter(signed_in=True).exclude(id=id)
    print('Signed in Users:', signed_in_users)

    # For any other user who is signed in, display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. 
    

    context = {
        'user_name': user_name,
        'all_followers': all_followers,
        'all_following': all_following,
        'all_posts': all_posts,
        'signed_in_users': signed_in_users
    }

    return render(request, 'network/profile.html', context)
