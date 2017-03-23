from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from .models import Post,Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "secret"
        ]



#http://stackoverflow.com/questions/28458770/how-can-create-a-model-form-in-django-with-a-one-to-one-relation-with-another-mo

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("birth_date",)

class UserForm(forms.ModelForm):
    password1 = forms.PasswordInput()
    #password2=forms.PasswordInput()
    #http://stackoverflow.com/questions/4939737/cant-add-field-to-modelform-at-init?rq=1
    class Meta:
        model = User
        fields = ('username',)

   

class SignUpForm(UserCreationForm):
    print "IN SIGNUP"
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    class Meta:
        print "IN META"
        model = User
        fields = ('username', 'email', 'birth_date','password1', 'password2', )

    #http://stackoverflow.com/questions/1160030/how-to-make-email-field-unique-in-model-user-from-contrib-auth-in-django
    def clean_email(self):
        print "IN UNIQUE EMAIL"
        email = self.cleaned_data.get('email')
        print email
        username = self.cleaned_data.get('username')
        print username
        print  User.objects.filter(email=email).exclude(username=username)
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email



class AxesCaptchaForm(forms.Form):
    captcha = CaptchaField()