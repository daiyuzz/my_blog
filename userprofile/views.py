from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import UserLoginForm


# Create your views here.

def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data清洗出合法的数据
            data = user_login_form.cleaned_data
            # 检验帐号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个user对象
            user = authenticate(data['username'],password=data['password'])
            if user:
                # 将用户数据保存在session中，即实现了登录动作
                login(request,user)
                return redirect("article:article_list")
            else:
                return HttpResponse("帐号或密码输入有误，请重新输入")
        else:
            return HttpResponse("帐号或密码输入不合法")
    elif request.method == "GET":
        user_login_form = UserLoginForm()
        context = {'form':user_login_form}
        return render(request,'userprofile/login.html',context)


def user_logout(request):
    logout(request)
    return redirect('article:article_list')