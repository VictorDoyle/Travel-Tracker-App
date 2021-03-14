from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.db.models import signals
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from .models import City, Profile, Post
from .forms import Post_Form, City_Form, SignUpForm, Profile_Form
from account.models import Account
# from django.contrib import messages

# Create your views here.
# email = EmailMessage(
#     email_subject,
#     email_body,
#     from_email,
#     to_list,
# )
# email.send(fail_silently=False)

# ===========================home page ==========================


def homepage(request):
    error_message = ''
    if request.method == "POST":
        if request.POST.get('submit') == 'Sign Up':
            add_form = SignUpForm(request.POST)
            if add_form.is_valid():
                user = add_form.save()
                login(request, user)

                # email_subject = "Welcome to Wayfarer"
                # email_body = "You have successfully signed up for an account!"
                # from_email = settings.EMAIL_HOST_USER
                # new_user_email = user.email
                # to_list = [new_user_email]
                # send_mail(
                #     email_subject,
                #     email_body,
                #     from_email,
                #     to_list,
                #     fail_silently=True,
                # )
                return redirect('profile')
            else:
                error_message = "Invalid Sign Up - Please Try Again"
        elif request.POST.get('submit') == 'Sign In':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                error_message = "Invalid Sign In Credentials - Please Try Again"
    form = SignUpForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'homepage.html', context)


def logout(request):
    logout(request)
    return redirect('homepage')


# ===================== Profile =========================

@login_required(login_url='/profile/')
def profile(req):
    # user = User.objects.get(user_id=req.user_id)
    # user.save()
    if req.method == 'POST':
        form = Post_Form(req.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = req.user
            new_post.save()
            return redirect('profile')

    if req.method == 'POST':
        city_form = City_Form(req.POST)
        if city_form.is_valid():
            new_city = city_form.save(commit=False)
            new_city.user = req.user
            new_city.save()
            return redirect('profile')

    # posts The users post
    posts = Post.objects.filter(user=req.user)
    # all citys
    cities = City.objects.filter(user=req.user)
    # profile
    profile = Profile.objects.get(user=req.user)
    post_form = Post_Form()
    city_form = City_Form()

    if req.method == 'POST':
        edit_form = Profile_Form(req.POST, instance=profile)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('profile')

    edit_form = Profile_Form(instance=profile)

    context = {'city': city, 'city_form': city_form, 'cities': cities, 'posts': posts,
               'post_form': post_form, 'profile': profile, 'edit_form': edit_form}
    return render(req, 'profile.html', context)


def profile_show(req, profile_id, city_id):
    if req.method == 'POST':
        form = Post_Form(req.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = req.user
            new_post.save()
            return redirect(req.get_full_path())

    if req.method == 'POST':
        city_form = City_Form(req.POST)
        if city_form.is_valid():
            new_city = city_form.save(commit=False)
            new_city.user = req.user
            new_city.save()
            return redirect(req.get_full_path())

    city = City.objects.get(id=city_id)
    # posts The users post
    posts = Post.objects.filter(city=city_id)
    # all citys
    cities = City.objects.filter(user=req.user)
    # profile
    profile = Profile.objects.get(user=req.user)
    post_form = Post_Form()
    city_form = City_Form()

    if req.method == 'POST':
        edit_form = Profile_Form(req.POST, instance=profile)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('profile')

    edit_form = Profile_Form(instance=profile)

    context = {'city': city, 'city_form': city_form, 'cities': cities, 'posts': posts,
               'post_form': post_form, 'profile': profile, 'edit_form': edit_form}
    return render(req, 'profile_show.html', context)


@login_required(login_url='/profile/')
def profile_detail(req, profile_id):
    user = Profile.objects.get(id=profile_id)
    if req.method == 'POST':
        edit_form = Profile_Form(req.POST, instance=profile)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('profile_detail', profile_id=profile.id)
    edit_form = Profile_Form(instance=user)
    context = {'user': user, 'edit_form': edit_form}
    return render(req, 'profile_detail.html', context)


@login_required(login_url='/profile/')
def profile_edit(req, profile_id):
    profile = Profile.objects.get(id=profile_id)
    if req.method == 'POST':
        edit_form = Profile_Form(req.POST, instance=profile)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('profile')

    edit_form = Profile_Form(instance=profile)
    context = {'edit_form': edit_form, 'user': profile}
    return render(req, 'profile_detail.html', context)


# ===========================Posts pages ==========================

@login_required(login_url='/profile/')
def post(req, post_id):
    post = Post.objects.get(id=post_id)
    # if request.method == "POST":
    #     title = request.POST['title']
    #     content = request.POST['content']
    #     username_form = request.POST['username']
    post_form = Profile_Form(instance=post)
    edit_form = Post_Form(instance=post)
    city_form = City_Form()
    context = {'post': post, 'post_form': post_form,
               'edit_form': edit_form, 'city_form': city_form}
    return render(req, 'post.html', context)


@login_required(login_url='/profile/')
def posts_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    post_form = Profile_Form(instance=post)
    edit_form = Post_Form(instance=post)
    cities = City.objects.all()
    context = {'post': post, 'post_form': post_form,
               'edit_form': edit_form, 'cities': cities}
    return render(request, 'post.html', context)


@login_required(login_url='/profile/')
def post_edit(req, post_id):
    post = Post.objects.get(id=post_id)
    if req.method == 'POST':
        edit_form = Post_Form(req.POST, instance=post)
        if edit_form.is_valid():
            edit_form.save()
            return redirect(req.get_full_path())

    edit_form = Post_Form(instance=post)
    context = {'edit_form': edit_form, 'post': post}
    return render(req, 'post.html', context)


@login_required(login_url='/profile/')
def posts(req):
    posts = Post.objects.all()
    city_form = City_Form()
    cities = City.objects.filter(user=req.user)
    profile = Profile.objects.get(user=req.user)
    context = {'posts': posts, 'cities': cities,
               'profile': profile, 'city_form': city_form}
    return render(req, 'posts.html', context)


def post_delete(req, post_id):
    Post.objects.get(id=post_id).delete()
    return redirect('all_posts')

# ===========================City pages ==========================


@login_required(login_url='/profile/')
def city(req):
    # create
    if req.method == 'POST':
        city_form = City_Form(req.POST)
        if city_form.is_valid():
            new_city = city_form.save(commit=False)
            new_city.user = req.user
            new_city.save()
            return redirect('profile')

    context = {'city': city, 'posts': posts}
    return redirect('profile')
    # return render(req, 'cities/index.html', context)


@login_required(login_url='/profile/')
def city_detail(req, slug):
    # create
    if req.method == 'POST':
        city_form = City_Form(req.POST)
        if city_form.is_valid():
            new_city = city_form.save(commit=False)
            new_city.user = req.user
            new_city.save()
            return redirect(req.get_full_path())
    cities = City.objects.all()
    inner_qs = City.objects.filter(name__contains=slug)
    posts = Post.objects.filter(city__in=inner_qs)
    post_form = Post_Form()
    city = City.objects.get(name=slug)
    city_form = City_Form()
    # posts of the city
    # posts = Post.objects.filter(city.pk=slug)
    # profile
    profile = Profile.objects.all()
    context = {'city': city, 'city_form': city_form,
               'post_form': post_form, 'posts': posts, 'profile': profile, 'cities': cities}
    return render(req, 'cities/detail.html', context)


@login_required
def city_edit(req, slug):
    city = City.objects.get(name=slug)
    if req.method == 'POST':
        city_form = City_Form(req.POST, instance=city)
        if city_form.is_valid():
            city_form.save()
            return redirect('city_detail', city)

    city_form = City_Form(instance=city)
    context = {'city_form': city_form, 'city': city}
    return render(req, 'cities/edit.html', context)
