from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from app.models import Category

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username, email, password)
        user.save()
        return True

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    def auth(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # the password verified for the user
                if user.is_active:
                    print("User is valid, active and authenticated")
                else:
                    print("The password is valid, but the account has been disabled!")
            else:
                # the authentication system was unable to verify the username and password
                print("The username and password were incorrect.")
            self.resp = user.id
            return True


class ForgotPassForm(forms.Form):
    email = forms.EmailField()


class CategoryForm(forms.ModelForm):
    class Meta:
            model = Category
            fields = ['name']