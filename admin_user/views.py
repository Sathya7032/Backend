from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .serializer import *
from app.models import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserDetailForm, AdminPasswordChangeForm


def index(request):
    return render(request,"index.html")


def home(request):
    user_codes = CodeSnippet.objects.filter(user=request.user)  # Assuming you're using Django's built-in authentication
    topics = TutorialPost.objects.filter(user=request.user) 
    blog = Blogs.objects.filter(user=request.user) 
    meme = Meme.objects.filter(user=request.user)
    return render(request, 'user/homepage.html', {'user_codes': user_codes,'topics':topics,'blog':blog,'meme':meme})

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            messages.success(request, f'Welcome {username}!')
            return redirect('homepage')
        else:
            messages.error(request, 'Username or password is incorrect or you do not have access.')
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form, 'title': 'Log in'})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def MemePostCreateView(request):
    if request.method == 'POST':
        description = request.POST.get('description', '')  # Fixed incorrect variable names
        images = request.FILES.get('images', None)  # Assuming you are uploading an image
        if description and images:  # Checking if both description and image are provided
            meme = Meme(description=description, images=images, user=request.user)  # Assigning the logged-in user to the meme
            meme.save()
            messages.success(request, "Meme added successfully.")
            return redirect('/homepage/')
        else:
            messages.error(request, "Please provide both description and image.")
    
    return render(request, "user/createMeme.html")

@login_required
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        if title and content:
            blog = Blogs(title=title, content=content, user=request.user)
            blog.save()
            messages.success(request, "Blog post created successfully.")
            return redirect('/homepage/')  # Adjust as needed
        else:
            messages.error(request, "Please provide both title and content.")
    return render(request, 'user/createBlog.html')

@login_required
def CodePostCreateView(request):
    if request.method == 'POST':
        form = CodeSnippetForm(request.POST, request.FILES)
        if form.is_valid():
            code_snippet = form.save(commit=False)
            code_snippet.user = request.user
            code_snippet.save()
            messages.success(request, "Code snippet added successfully.")
            return redirect('/homepage/')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CodeSnippetForm()

    return render(request, "user/createCode.html", {'form': form})

@login_required
def add_topic(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Topic added successfully.")
            return redirect('/post_code/')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TopicForm()
    return render(request, "user/add_topic_modal.html", {'form': form})


@login_required
def create_language(request):
    if request.method == 'POST':
        language = request.POST.get('language', '')
        if language :
            lang = Language(language=language)
            lang .save()
            messages.success(request, "Language is created successfully.")
            return redirect('/add_language/')  # Adjust as needed
        else:
            messages.error(request, "Please provide both title and content.")
    return render(request, 'user/createLanguage.html')


@login_required
def TutorialTopicCreateView(request):
    if request.method == 'POST':
        form = TutorialTopicForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data
            tutorial_topic = form.save(commit=False)
            # Assign the current user to the tutorial topic
            tutorial_topic.user = request.user
            tutorial_topic.save()
            messages.success(request, "Tutorial Topic added successfully.")
            # Redirect to the homepage or any appropriate page
            return redirect('/homepage/')
        else:
            # If form is not valid, display error messages
            messages.error(request, "Please correct the errors below.")
    else:
        # If request method is GET, create a new empty form
        form = TutorialTopicForm()

    # Render the form page, whether it's GET or POST
    return render(request, "user/createTutTopic.html", {'form': form})

@login_required
def create_tutorial(request):
    if request.method == 'POST':
        form = TutorialForm(request.POST, request.FILES)
        if form.is_valid():
            tutorial = form.save(commit=False)
            tutorial.user = request.user  # Assign the current user to the tutorial
            tutorial.save()
            messages.success(request, "Tutorial added successfully.")
            return redirect('/add_post/')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TutorialForm()

    return render(request, "user/add_tutorial.html", {'form': form})


@login_required
def blogSingle(request, id):
    blogs = get_object_or_404(Blogs, id=id)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            blogs.delete()
            messages.success(request, "Blog is deleted successfully.")
            return redirect('/homepage/')  
        
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        # Basic validation
        if title and content:
            blogs.title = title
            blogs.content = content
            blogs.save()
            messages.success(request, "Blog is edited successfully.")
            return redirect('/homepage/')  # Redirect to a detail view or another page
        else:
            messages.error(request,'Something went wrong')
    return render(request, 'user/singleBlog.html', {'blogs': blogs})



def CodeSingle(request, code_id):
    snippet = get_object_or_404(CodeSnippet, code_id=code_id)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            snippet.delete()
            messages.success(request, "Code is Deleted successfully.")
            return redirect('/homepage/')  # Redirect to the homepage or another page after deletion

        form = CodeSnippetForm(request.POST, instance=snippet)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Code is edited successfully.")
            return redirect('/homepage/')  # Redirect to a detail view or another page
    
    else:
        messages.error(request, "Something went wrong")
        form = CodeSnippetForm(instance=snippet)

    return render(request, 'user/singleCode.html', {'form': form, 'snippet': snippet})



def topicSingle(request, post_id):
    snippet = get_object_or_404(TutorialPost, post_id=post_id)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            snippet.delete()
            messages.success(request, "Tutorial topic is Deleted successfully.")
            return redirect('/homepage/')  # Redirect to the homepage or another page after deletion

        form = TutorialTopicForm(request.POST, instance=snippet)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Tutorial topic is edited successfully.")
            return redirect('/homepage/')  # Redirect to a detail view or another page
    
    else:
        messages.error(request, "Something went wrong")
        form = TutorialTopicForm(instance=snippet)

    return render(request, 'user/singleTopic.html', {'form': form, 'snippet': snippet})


@login_required
def MemeSingle(request, id):
    meme = get_object_or_404(Meme, id=id)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            meme.delete()
            messages.success(request, "Meme deleted successfully.")
            return redirect('/homepage/')  
        
        description = request.POST.get('description')
        images = request.FILES.get('images')
        
        # Basic validation
        if description:
            meme.description = description
        if images:
            meme.images = images
        
        if description or images:
            meme.save()
            messages.success(request, "Meme edited successfully.")
            return redirect('/homepage/')  # Redirect to a detail view or another page
        else:
            messages.error(request, "Please provide a new description or image to update the meme.")
    return render(request, 'user/SingleMeme.html', {'meme': meme})


@login_required
@staff_member_required
def admin_user_detail(request):
    if request.method == 'POST':
        user_form = UserDetailForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('admin_user_detail')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserDetailForm(instance=request.user)

    return render(request, 'user/admin_user_detail.html', {
        'user_form': user_form,
    })

@login_required
@staff_member_required
def admin_user_password_change(request):
    if request.method == 'POST':
        password_form = AdminPasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important to update the session with new password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('admin_user_password_change')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        password_form = AdminPasswordChangeForm(request.user)

    return render(request, 'user/admin_user_password_change.html', {
        'password_form': password_form,
    })
    

@login_required
@staff_member_required
def profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'user/profile.html', context)

def error_404(request, exception):
    return render(request, 'user/505_404.html', status=404)
 
def error_500(request):
    return render(request, 'user/505_404.html', status=500)
