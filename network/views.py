from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Required for edit function.
import json
from django.http import JsonResponse

from .models import User, Post, Follow

from .forms import CreatePostForm


def index(request):

    """
    All Posts: The “All Posts” link in the navigation bar should take the user to a page where they can see all posts from all users, with the most recent posts first.
    https://docs.djangoproject.com/en/5.0/ref/models/querysets/#order-by - The negative sign in front of "-created" indicates descending order.
    """
    all_posts = Post.objects.all().order_by('-created')
    # print('All Index Posts:', all_posts )

    # Pagination - https://docs.djangoproject.com/en/5.0/topics/pagination/
    paginator = Paginator(all_posts, 10) # Show 10 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Include the “New Post” form before “All Posts” on index.html. 
    form = CreatePostForm()

    context = {
        "all_posts": all_posts,
        "form": form,
        "page_obj": page_obj
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
    # print('Current User:', user_name)
    user_id = request.user.id
    
    # Get number of followers the user has and the number of people the user follows.
    # https://stackoverflow.com/questions/58794639/how-to-make-follower-following-system-with-django-model
    user = User.objects.get(id=id) # ID for the current user.
    # all_followers are users who are following the current user.
    all_followers = len(user.following.all())
    # print('Followers:', all_followers)
    # all_following are all users who the current user is following. 
    all_following = len(user.followers.all())
    # print('Following:', all_following)

    # Display all of the posts for that user, in reverse chronological order.
    all_posts = user.user.all().order_by('-created')
    # print('All Posts:', all_posts)

    # Pagination - https://docs.djangoproject.com/en/5.0/topics/pagination/
    paginator = Paginator(all_posts, 10) # Show 10 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Get all users who are signed in.
    # If a user is signed in, signed_in == true. This list should not include the user on this page.
    # https://stackoverflow.com/questions/2354284/django-queries-how-to-filter-objects-to-exclude-id-which-is-in-a-list
    # https://docs.djangoproject.com/en/5.0/topics/db/queries/#retrieving-specific-objects-with-filters
    # exclude(**kwargs) - Returns a new QuerySet containing objects that do not match the given lookup parameters.
    signed_in_users = User.objects.filter(signed_in=True).exclude(id=id)
    # print('Signed in Users:', signed_in_users)

    # For any other user who is signed in, display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. 
    # If the current user is not following a signed in user, they may follow them. If the current user is following a signed in user, they may unfollow them.
    #     
    current_user_is_following = user.followers.values_list('user_follows_id', flat=True)
    current_user_is_following_ids = []
    for i in current_user_is_following:
        current_user_is_following_ids.append(i)

    # print('current_user_is_following:', current_user_is_following)    
    # print('current_user_is_following_ids:', current_user_is_following_ids)    

    context = {
        'user_name': user_name,
        'all_followers': all_followers,
        'all_following': all_following,
        'all_posts': all_posts,
        'signed_in_users': signed_in_users,
        'current_user_is_following_ids': current_user_is_following_ids,
        'page_obj': page_obj
    }

    return render(request, 'network/profile.html', context)


"""
Follow and Unfollow Functions
"""

def follow(request, user):

    user_id = request.user.id

    # user_to_follow = user # user == user_name and I need the user's id
    user_to_follow_id = User.objects.get(username=user).id
    # print('user_to_follow_id:', user_to_follow_id)

    # https://medium.com/@abdullafajal/step-by-step-guide-to-implement-follow-unfollow-functionality-in-django-f98dd501aa36
    # Create a row with the current user and the user to follow to the database.
    Follow.objects.create(
        following_user_id=user_id, #follower
        user_follows_id=user_to_follow_id #following
    )

    user = User.objects.get(id=user_id) # ID for the current user.
    current_user_is_following = user.followers.values_list('user_follows_id', flat=True)
    current_user_is_following_ids = []
    for i in current_user_is_following:
        current_user_is_following_ids.append(i)

    print('current_user_is_following:', current_user_is_following)
    
    print('current_user_is_following_ids:', current_user_is_following_ids)

    # Send all necessary data to build profile.html again.
    user_name = request.user

    user = User.objects.get(id=user_id)
    all_followers = len(user.following.all())
    all_following = len(user.followers.all())
    all_posts = user.user.all().order_by('-created')
    signed_in_users = User.objects.filter(signed_in=True).exclude(id=user_id)

    context = {           
        'user_name': user_name,
        'all_followers': all_followers,
        'all_following': all_following,
        'all_posts': all_posts,
        'signed_in_users': signed_in_users,
        'current_user_is_following_ids': current_user_is_following_ids
    }

    # return HttpResponseRedirect(reverse('profile', args=(user_id,))) # To send context to profile.html, I must render because reverse only returns a url string.
    return render(request, 'network/profile.html', context)


def unfollow(request, user):

    user_id = request.user.id

    user_to_unfollow_id = User.objects.get(username=user).id
    print('user_to_unfollow_id', user_to_unfollow_id)

    # https://stackoverflow.com/questions/3805958/how-to-delete-a-record-in-django-models
    # Remove the row with the current user and the user to unfollow from the database.
    Follow.objects.filter(following_user_id=user_id).filter(user_follows_id=user_to_unfollow_id).delete()

    user = User.objects.get(id=user_id) # ID for the current user.
    current_user_is_following = user.followers.values_list('user_follows_id', flat=True)
    current_user_is_following_ids = []
    for i in current_user_is_following:
        current_user_is_following_ids.append(i)

    # print('current_user_is_following:', current_user_is_following)    
    # print('current_user_is_following_ids:', current_user_is_following_ids)    

    # Send all necessary data to build profile.html again.
    user_name = request.user

    user = User.objects.get(id=user_id)
    all_followers = len(user.following.all())
    all_following = len(user.followers.all())
    all_posts = user.user.all().order_by('-created')
    signed_in_users = User.objects.filter(signed_in=True).exclude(id=user_id)

    context = {              
        'user_name': user_name,
        'all_followers': all_followers,
        'all_following': all_following,
        'all_posts': all_posts,
        'signed_in_users': signed_in_users,
        'current_user_is_following_ids': current_user_is_following_ids
    }

    # return HttpResponseRedirect(reverse('profile', args=(user_id,)))
    return render(request, 'network/profile.html', context)


"""
Following Page: Display all posts made by users that the current user follows.
This page should behave just as the “All Posts” page does, just with a more limited set of posts.
This page should only be available to users who are signed in.

"""

# https://cs50.harvard.edu/web/2020/projects/2/commerce/#hints
# https://docs.djangoproject.com/en/5.0/topics/auth/default/#the-login-required-decorator
# Adding the @login_required decorator on top of any view will ensure that only a user who is logged in can access that view.
@login_required
def following(request, id):

    # id = request.user.id

    user = User.objects.get(id=id)
    all_following = user.followers.all()
    # print('All Following', all_following)

    all_following_ids = []
    for i in all_following:
        # Get the id for each user the current user follows.
        # print('i', User.objects.get(username=i).id)
        all_following_ids.append(User.objects.get(username=i).id)

        # print('All Following Ids', all_following_ids)

    all_following_posts = [] # Returns a list inside another list. Requires a nested loop in following.html.
    # Get all posts for each id in the list all_following_ids.
    for i in all_following_ids:
        all_following_posts.append(Post.objects.filter(author=i))

        # print('All Following Posts', all_following_posts)

    # Pagination - https://docs.djangoproject.com/en/5.0/topics/pagination/
    paginator = Paginator(all_following_posts, 10) # Show 10 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Research documentation below. This may be an alternative strategy to get the related data.
    # https://stackoverflow.com/questions/13092268/how-do-you-join-two-tables-on-a-foreign-key-field-using-django-orm
    # https://docs.djangoproject.com/en/5.0/ref/models/querysets/#select-related 
    # for i in all_following:
    #     all_following_posts = Post.objects.select_related('post').get(author=i)    
    #     print('All Following Posts', all_following_posts)
    # ValueError at /following1 Cannot query "Shirley": Must be "User" instance.
           
    context = {
        'all_following_posts': all_following_posts,
        'page_obj': page_obj
    }

    return render(request, 'network/following.html', context)


"""
Edit Post: Users should be able to click an “Edit” button or link on any of their own posts to edit that post.
When a user clicks “Edit” for one of their own posts, the content of their post should be replaced with a textarea where the user can edit the content of their post.
The user should then be able to “Save” the edited post. Using JavaScript, you should be able to achieve this without requiring a reload of the entire page.
For security, ensure that your application is designed such that it is not possible for a user, via any route, to edit another user’s posts.

"""

def edit(request, post_id):

    if request.method == 'POST': 
        # Edit post with the new data from the user. 
        data = json.loads(request.body)
        # print('Data:', data) 
        # print('Post id:', post_id)

        # post_to_update = Post.objects.filter(pk=post_id) # Returns a QuerySet
        post_to_update = Post.objects.get(pk=post_id) # Returns a single object
        # print('Post to Update:', post_to_update)

        revised_post = data['post']
        # Set the Post object's post attribute equal to the revised post data from the user.
        post_to_update.post = revised_post

        # Save the revised post.
        post_to_update.save()

        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status - 201 Created
        return JsonResponse({"message": "Post updated successfully."}, status=201)