from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import BlogForm, LoginForm, UserForm
from .models import Blog
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse

# Create your views here.
def layout(request):
    return render(request, 'app/layout.html')

def index(request):
    blogs = Blog.objects
    return render(request, 'app/index.html', {'blogs': blogs})

def new(request):
    return render(request, 'app/new.html')

def create(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/app/index/')

def blogform(request, blog=None):
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.pub_date = timezone.datetime.now()
            blog.save()
            return redirect('index')
    else:
        form = BlogForm(instance=blog)
        return render(request, 'app/new.html', {'form':form})

def edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return blogform(request, blog)

def remove(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    return redirect('index')

def detail(request, blog_id):
        blog_detail = get_object_or_404(Blog, pk=blog_id)
        return render(request, 'app/detail.html', {'blog':blog_detail})

def signin(request):
        if request.method == "POST":
                form = LoginForm(request.POST)
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username = username, password = password)

                if user is not None:
                        login(request, user)
                        return redirect('index')
                else:
                        return HttpResponse('로그인 실패, 다시 시도 해보세요.')
        else:
                form = LoginForm()
                return render(request, 'app/signin.html', {'form':form})

def signup(request):
        if request.method == "POST":
                form = UserForm(request.POST)
                if form.is_valid():
                        new_user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
                        login(request, new_user)
                        return redirect('index')
        else:
                form = UserForm()
                return render(request, 'app/signup.html', {'form':form})