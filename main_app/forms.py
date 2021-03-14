from django import forms
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post, City, Profile
from .models import Account

# from .models import

# from accounts.models import UserProfile


# class EditProfileForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['username','password', 'cities', 'avatar']

# class ProfileForm(ModelForm):
#          class Meta:
#             model = User
#             fields = ['username','password','cities']


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('cities', 'country') #Note that we didn't mention user field here.

#     def save(self, user=None):
#         user_profile = super(UserProfileForm, self).save(commit=False)
#         if user:
#             user_profile.user = user
#             user_profile.save()
#             return user_profile


# og submaster

class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control'}))


    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

   

class Post_Form(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'city']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
        }


class City_Form(ModelForm):
    class Meta:
        model = City
        fields = ['name', 'description', 'flags']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'flags': forms.TextInput(attrs={'class': 'form-control'}),
        }


class Profile_Form(ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'city', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
        }
