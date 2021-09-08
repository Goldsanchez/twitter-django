from django.shortcuts import get_object_or_404, render, redirect
from .models import Post, Profile, Relationship
from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm, se cambio a userregistracion porque lo hereda
from .forms import PostForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def feed(request):
    posts = Post.objects.all() #Para posts
    pk=request.user.pk
    #current_user = get_object_or_404(User, ) # para form de posts
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = pk
            post.save()
            messages.success(request, 'Post Enviado')
            return redirect('feed')
    else:
        form = PostForm()

    context = {'posts': posts, 'form': form}
    return render(request, 'app_social/feed.html', context)

def profile(request, username=None):

    

    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
    else:
        posts = current_user.posts.all()
        user = current_user

    return render(request, 'app_social/profile.html', {'user': user, 'posts': posts})


def register(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return redirect('feed')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'app_social/register.html', context)


def post(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            messages.success(request, 'Post Enviado')
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'app_social/post.html', {'form': form})

@login_required
def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship(from_user=current_user, to_user = to_user_id)
    rel.save()
    messages.success(request, f'Sigues a {username}')
    return redirect('feed')

@login_required
def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user.id
    rel = Relationship.objects.filter(from_user=current_user.id, to_user = to_user_id).get()
    rel.delete()
    messages.success(request, f'Ya no sigues a {username}')
    return redirect('feed')