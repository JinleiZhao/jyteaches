from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class Login_Form(forms.Form):
    username = forms.CharField(required=True) #不能为空,名字与前端的name名字一样
    password = forms.CharField(required=True,min_length=5,error_messages={"required":"密码错误"})


class Register_Form(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=5)
    captcha = CaptchaField()


class ForgetPwd_Form(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()

class ResetPwd_Form(forms.Form):
    password1 = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True,min_length=5)

class UserInfo_Form(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nike_name","sex","birthday","address","mobile"]

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]
