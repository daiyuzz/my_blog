from django import forms
from django.contrib.auth.models import User


# 登录表单，继承了forms.Form类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()