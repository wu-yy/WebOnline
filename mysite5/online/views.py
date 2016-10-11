from django.shortcuts import render,render_to_response
from  django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django import forms
from online.models import  User

# Create your views here.
#表单
class UserForm(forms.Form):
    username=forms.CharField(label='用户名',max_length=100)
    password=forms.CharField(label='密码',widget=forms.PasswordInput())

#注册
def regist(req):
    if req.method=='POST':
        uf=UserForm(req.POST)
        if uf.is_valid():
            #获取表单数据
            username=uf.cleaned_data['username']
            password=uf.cleaned_data['password']
            #添加到数据库
            User.objects.create(username=username,password=password)
            return HttpResponse('regist success!')
    else:
        uf=UserForm()
    return render_to_response('regist.html',{'uf':uf})

#登录
def login(req):
    if req.method=='POST':
        uf=UserForm(req.POST)
        if uf.is_valid():
            username=uf.cleaned_data['username']
            password=uf.cleaned_data['password']
            user=User.objects.filter(username__exact=username,password__exact=password)

            if user:
                response=HttpResponseRedirect('/online/index/')
                response.set_cookie('username',username,3600)
                return response
            else:
                return HttpResponseRedirect('/online/login/')
    else:
        uf=UserForm()
    return render_to_response('login.html',{'uf':uf})
#登录成功
def index(req):
    username=req.COOKIES.get('username','')
    return render_to_response('index.html',{'username':username})

#退出
def logout(req):
    response=HttpResponse('logout!!')
    response.delete_cookie('username')
    return response

