from django.shortcuts import render, redirect,reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model,login,logout
from django.contrib.auth.models import User
User = get_user_model()

from .forms import RegisterForm, LoginForm
from .models import CaptchaModel

# Create your views here.
@require_http_methods(['GET','POST'])
def xxlogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                if not remember:
                    #如果没有点击记住我，那么就要设置过期时间位0，即浏览器关闭后就会国企
                    request.session.set_expiry(0)
                #如果点击了，就什么都不做，默认两周过期时间
                return redirect('/')
            else:
                # form.add_error('email','邮箱或者密码错误')
                # return render(request, 'login.html',context={'form':form})
                return redirect(reverse('myauth:login'))
        return None
def xxlogout(request):
    logout(request)
    return redirect(reverse('myauth:login'))

@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse('myauth:login'))
        else:
            print(form.errors)
            return render(request, 'register.html',context={'form':form})

def send_email_captcha(request):
    # ?email=xxx
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message": '必须传递邮箱'})
    # 生成验证码（取随机4位数字）
    captcha = "".join(random.sample(string.digits, 4))
    # 保存到数据库中
    CaptchaModel.objects.update_or_create(email=email,defaults={'captcha':captcha})

    send_mail("嘻嘻博客注册验证码", message=f"您的注册验证码是:{captcha}", recipient_list=[email], from_email=None)
    return JsonResponse({"code": 200, "message": "邮箱发送成功"})
