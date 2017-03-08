from django import forms
from .models import Story, StoryComment, Profile, PostReport
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re


class PostStoryForm(forms.ModelForm):
    # It is the form used for posting a new story.
    class Meta:
        model = Story
        fields = ['title', 'text', 'category', 'language',]

        widgets = {
            'title': forms.TextInput(attrs={
                'autocomplete': 'off',
                'size': 60,
                'class': 'form-control'}),
            'text': forms.Textarea(attrs={
                'rows': 20,
                'cols': 60,
                'class': 'form-control'}),
            'category': forms.Select(attrs={
                'id': 'profile',
                'class': 'form-control'}),
            'language': forms.Select(attrs={
                'id': 'profile',
                'class': 'form-control'})
        }


    def clean_title(self):
        # This method checks title's validation status.
        # It must have 160 characters at most.
        title = self.cleaned_data.get('title')
        if len(title) > 160:
            raise forms.ValidationError("Title must contain maximum 160 characters.")
        return title


    def clean_text(self):
        # This method checks post text's validation status.
        # It must have at least 10 at most 3000 characters.
        text = self.cleaned_data.get('text')
        if len(text) > 3000 or len(text) < 10:
            raise forms.ValidationError('Your Story must contain maximum 3000 characters.')
        return text



class LoginForm(forms.Form):
    # It is the form used for logging a existing user in.
    username = forms.CharField(max_length=13, widget = forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=20, widget = forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        # It checks if there is a user named 'username' and if it is active or not.
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_qs = User.objects.filter(username=username)
        if user_qs.count() == 0:
            raise forms.ValidationError("This user does not exist!")
        else:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Incorrect password!")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
        return super(LoginForm, self).clean(*args, **kwargs)


class SignupForm(forms.ModelForm):
    # It is the form used for signing a new user up.
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={
        'autocomplete': 'off',
        'class': 'form-control',
        'required': 'required'}))

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={
                'autocomplete': 'off',
                'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={
                'autocomplete': 'off',
                'class': 'form-control'}),
            'email': forms.EmailInput(attrs={
                'autocomplete': 'off',
                'class': 'form-control',
                'required': 'required'}),
        }

    def clean_password2(self):
        # It checks if emails fields are identical.
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password == "" or password is None:
            raise ValidationError("You cannot leave Password field empty!")
        if password != password2:
            raise forms.ValidationError("Passwords are not matched")
        return password2

    def clean_username(self):
        # It checks if 'username' consists of alphabetical and numerical characters.
        username = self.cleaned_data.get('username')
        exp = re.compile('[^a-zA-Z0-9_]')
        if re.search(exp, username):
            raise forms.ValidationError("Username must only contain upper or lower letters, numbers or '_' character.")
        if len(username) < 4 and len(username) > 15:
            raise forms.ValidationError("Username must have 5 characters at least and 14 characters at most!")
        username_check = User.objects.filter(username=username)
        if username_check.exists():
            raise forms.ValidationError("Username is already taken!")
        return username

    def clean_email(self):
        # It checks if email address is already registered.
        email = self.cleaned_data.get('email')
        email_check = User.objects.filter(email=email)
        if email_check.exists():
            raise forms.ValidationError('Email has already been registered')
        return email


class SearchPostForm(forms.Form):
    # This form is the search engine of the site.
    searchq = forms.CharField(label="Search Post", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'maxlength': '25',}))


class UserEditForm(forms.ModelForm):
    # This form lets users edit their profile details.
    class Meta:

        model = User
        fields = [
            'email', 'first_name', 'last_name',
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'autocomplete': 'off',
                'size': 60,
                'class': 'form-control',}),
            'email': forms.EmailInput(attrs={
                'size': 60,
                'class': 'form-control',
                'required': 'required',}),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',}),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',})
        }

    def clean_email(self):
        # email field shouldn't be empty
        email = self.cleaned_data.get('email')
        if email is None or email == "":
            raise forms.ValidationError("You can't leave E-mail field blank!")
        return email

    """
    def clean_username(self):
        # username must have alphabetical or numerical characters only.
        username = self.cleaned_data.get('username')
        exp = re.compile('[^a-zA-Z0-9_]')
        if re.search(exp, username):
            raise forms.ValidationError("Username must only contain upper or lower letters, numbers or '_' character.")
        username_check = User.objects.filter(username=username)
        if username_check.exists():
            raise forms.ValidationError("Username is already taken!")
        if username == "" or username is None:
            raise forms.ValidationError("You cannot leave Username input Empty!")
        return username
    """

class ProfileEditForm(forms.ModelForm):
    # It allows to edit other profile details.
    class Meta:

        model = Profile
        fields = ['gender', 'birthday']

        widgets = {
            'gender': forms.Select(attrs={
                'autocomplete': 'off',
                'class': 'form-control',}),
            'birthday' : forms.DateInput(attrs={
                'class': 'form-control',})
        }


class LeaveComment(forms.ModelForm):
    # It allows users to leave a comment on a post.
    class Meta:

        model = StoryComment
        fields = ['comment']

        widgets = {
            'comment' : forms.Textarea(attrs={
                'autocomplete': 'off',
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Leave a comment',
                'required' : 'required',})
        }


class ReportStory(forms.ModelForm):
    # It allow users to report any of the posts.
    class Meta:
        model = PostReport
        fields = ['report_text']

        widgets = {
            'report_text' : forms.Textarea(attrs={
                'rows' : 20,
                'cols' : 60,
                'class' : 'form-control',}),
        }
