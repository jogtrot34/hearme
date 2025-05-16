from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from decimal import Decimal
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver




# Create your views here.
#Authenticcation type ting

def signup_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and get the instance

            # Automatically log the user in after registration
            login(request, user)

            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('home')  # Redirect to home or profile page

        else:
            # Handle specific form errors more gracefully
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserRegisterForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    context ={
        'form': form,
    }
    return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    return redirect('home')


#App views
def index_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    context={

    }
    return render(request, 'index.html', context)

def how_view(request):
    admin = User.objects.get(username='Jogtrot34')
    if request.user.is_authenticated:
        return redirect('home')
    context={
        'admin':admin,
    }
    return render(request, 'how.html', context)

@login_required
def home_view(request):
    posts = Post.objects.all().order_by('?')
    tags = PostTag.objects.all().order_by('?')[:10]
    user_tags = Post.objects.filter(author=request.user).values_list('tags__id', flat=True)
    similar_posts = Post.objects.filter(tags__id__in=user_tags).exclude(author=request.user)
    similar_users = User.objects.filter(posts__in=similar_posts).distinct()

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        tags_input = request.POST.get('tags', '')
        tag_names = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]

        if content:
            post = Post.objects.create(
                content=content,
                author=request.user
            )

            for name in tag_names:
                tag, created = PostTag.objects.get_or_create(name=name)
                post.tags.add(tag)

            return redirect('home')
    context={
        'posts':posts,
        'tags': tags,
        'sim': similar_users,
        'simp': similar_posts,
    }
    return render(request, 'feed.html', context)

@login_required
def comments_view(request, post_id):
    posts = Post.objects.all().order_by('?')
    post = get_object_or_404(Post, id=post_id)
    tags = PostTag.objects.all().order_by('?')[:10]
    user_tags = Post.objects.filter(author=request.user).values_list('tags__id', flat=True)
    similar_posts = Post.objects.filter(tags__id__in=user_tags).exclude(author=request.user)
    similar_users = User.objects.filter(posts__in=similar_posts).distinct()

    if request.method == 'POST':
        content = request.POST.get('comment', '').strip()

        if content:
            comment = Comment.objects.create(
                content=content,
                user=request.user,
                post=post
            )

            return redirect('comments', post_id=post_id)
    context={
        'posts':posts,
        'post':post,
        'tags': tags,
        'sim': similar_users,
        'simp': similar_posts,
    }
    return render(request, 'comments.html', context)

@login_required
def search_posts(request):
    query = request.GET.get('q', '')
    results = []
    user_tags = Post.objects.filter(author=request.user).values_list('tags__id', flat=True)
    similar_posts = Post.objects.filter(tags__id__in=user_tags).exclude(author=request.user)
    similar_users = User.objects.filter(posts__in=similar_posts).distinct()

    tags = PostTag.objects.all().order_by('?')[:10]
    if query:
        results = Post.objects.filter(
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    return render(request, 'feed.html', {
        'query': query,
        'posts': results,
        'tags': tags,
        'sim': similar_users,
    })


def posts_by_something(request, type, name):
    # Get common data (tags and recommendations)
    tags = PostTag.objects.all()[:10]
    user_tags = Post.objects.filter(author=request.user).values_list('tags__id', flat=True)
    similar_posts = Post.objects.filter(tags__id__in=user_tags).exclude(author=request.user)
    similar_users = User.objects.filter(posts__in=similar_posts).distinct()

    # Initialize posts queryset
    posts = Post.objects.none()  # Empty queryset to start

    type = str(type).lower()  # Normalize the type

    if 'tag' in type:
        tag = get_object_or_404(PostTag, name=name)
        posts = Post.objects.filter(tags=tag).select_related('author').prefetch_related('tags')

    elif 'user' in type:
        user = get_object_or_404(User, username=name)  # Typically use username rather than name
        posts = Post.objects.filter(author=user).select_related('author').prefetch_related('tags')


    context = {
        'posts': posts,
        'tags': tags,
        'sim': similar_users,
    }

    return render(request, 'feed.html', context)

def profile_view(request):


    return render(request, 'user.html', {
    })



@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@csrf_exempt  # If you're not using AJAX with CSRF token (NOT RECOMMENDED)
@login_required
def update_profile(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user
            profile = user.profile

            # Update user fields
            user.first_name = data.get("first_name", user.first_name)
            user.last_name = data.get("last_name", user.last_name)
            user.username = data.get("username", user.username)
            user.save()

            # Update profile fields
            profile.bio = data.get("bio", profile.bio)
            profile.location = data.get("location", profile.location)
            profile.personal_story = data.get("personal_story", profile.personal_story)

            # Update interests (assumes comma-separated)
            tags_raw = data.get("interests", "")
            profile.interests.clear()
            if tags_raw:
                tag_names = [tag.strip() for tag in tags_raw.split(",") if tag.strip()]
                for name in tag_names:
                    tag, created = PostTag.objects.get_or_create(name=name)
                    profile.interests.add(tag)

            profile.save()

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid method"})

@login_required
@require_POST
def hug_post(request):
    try:
        data = json.loads(request.body)
        post_id = data.get('post_id')
        post = Post.objects.get(id=post_id)

        hug, created = Hug.objects.get_or_create(user=request.user, post=post)

        # If hug already existed, delete it (toggle off)
        if not created:
            hug.delete()
            message = "Hug removed"
        else:
            message = "Hug added"

        return JsonResponse({
            'success': True,
            'hug_count': post.hugs.count(),
            'message': message
        })
    except Post.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Post not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def chat_list_view(request):
    user = request.user
    conversations = Conversation.objects.filter(user1=user) | Conversation.objects.filter(user2=user)

    # Extract the other participant from each conversation
    partners = []
    for convo in conversations:
        if convo.user1 == user:
            partners.append(convo.user2)
        else:
            partners.append(convo.user1)

    # Optionally remove duplicates if any (in case of broken data)
    unique_partners = list(set(partners))
    context={
        'users': unique_partners,
    }
    return render(request, 'messaging.html', context)

@login_required
def messages_view(request, username):
    user = request.user
    recipient = get_object_or_404(User, username=username)

    # Get or create conversation between users
    conversation = Conversation.objects.filter(
        Q(user1=user, user2=recipient) | Q(user1=recipient, user2=user)
    ).first()

    # If no conversation exists, create one
    if not conversation:
        conversation = Conversation.objects.create(user1=user, user2=recipient)

    # Get messages ordered by timestamp (oldest first)
    mess = Message.objects.filter(conversation=conversation).order_by('timestamp')
    if request.method == 'POST':
        content = request.POST.get('message', '').strip()

        if content:
            messa = Message.objects.create(
                content=content,
                sender=request.user,
                conversation=conversation,
            )
            return redirect('messages',username)
    context = {
        'u': recipient,
        'mess': mess,
        'conversation': conversation,
    }
    return render(request, 'chat.html', context)



def handler404(request, exception):
    return render(request, 'error_base.html', {
        'error_code': 404,
        'error_message': 'Page Not Found'
    }, status=404)

def handler500(request):
    return render(request, 'error_base.html', {
        'error_code': 500,
        'error_message': 'Server Error'
    }, status=500)

def handler403(request, exception):
    return render(request, 'error_base.html', {
        'error_code': 403,
        'error_message': 'Forbidden'
    }, status=403)

def handler400(request, exception):
    return render(request, 'error_base.html', {
        'error_code': 400,
        'error_message': 'Bad Request'
    }, status=400)