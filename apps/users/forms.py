# 用户注册表单验证
from captcha.fields import CaptchaField
from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8)
    captcha = CaptchaField(error_messages={'invalid': '验证码有误'})


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8)


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码有误'})


class NewPwdForm(forms.Form):
    pwd1 = forms.CharField(required=True, min_length=8)
    pwd2 = forms.CharField(required=True, min_length=8)