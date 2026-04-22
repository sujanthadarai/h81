from django.shortcuts import render,redirect
from .models import Contact,Category,Momo
import qrcode #pip install qrcode
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth import authenticate,login
import logging

logger=logging.getLogger("django")
# Create your views here.
# @login_required(login_url='log_in')
def index(request):
    category=None
    momo=None
    try:
        
        category=Category.objects.all()
        
        cate_id=request.GET.get('category') #2 or all
        if cate_id == 'all':
            momo=Momo.objects.all()
        elif cate_id:
            momo=Momo.objects.filter(category=cate_id)
        else:
            momo=Momo.objects.all()

            
        if request.method == 'POST':
            name=request.POST['name']
            phone=request.POST['phone']
            email=request.POST['email']
            message=request.POST['message']
            Contact.objects.create(name=name,phone=phone,message=message,email=email)
            return redirect('index')
        
    except Exception as e:
        logger.error(e,exc_info=True)
    
    context={
        'category':category,
        'momo':momo
        }
    
    return render(request,'core/index.html',context)

@login_required(login_url='log_in')
def about(request):
    return render(request,'core/about.html')

@login_required(login_url='log_in')
def menu(request):
    category=Category.objects.all()
    qr=qrcode.make(f"http://127.0.0.1:8000/{request.path}")
    qr.save("core/static/images/menu.png")
    return render(request,'core/menu.html',{'category':category})


'''  
Authentication (who are you?) : the process of verify your identity
Authorization : what are you allowed to do after login 
'''
'''
====================================================================
                            Authentication
====================================================================
'''
def register(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password'] #abc
        password1=request.POST['password1'] #abc
        
        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.error(request,'username is already exists')
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.error(request,'email is already exists')
                return redirect('register')
            
            if not re.search(r'[A-Z]',password) :
                messages.error(request,'your password must contain  at least one uppercase')
                return redirect('register')
            if not re.search(r"\d",password):
                messages.error(request,"password must contain at least one digit!!!")
                return redirect('register')
                
            
            try:
                validate_password(password) #abc
                User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
                messages.success(request,"account create successfully!!!")
                return redirect('register')
            except ValidationError as e:
                for i  in e.messages:
                    messages.error(request,i)
                return redirect('register')
                
        else:
            messages.error(request,"password and confirm password doesnot match")
            return redirect('register')
            
        
        
    return render(request,'accounts/register.html')


from django.contrib.auth import authenticate,login,logout

def log_in(request):
    if request.method == 'POST':
        username=request.POST.get('username') #abcd
        password=request.POST.get('password') #Ramm710@
        remember_me=request.POST.get('remember_me') #on or None
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,'username is not register yet!!!')
            return redirect('log_in')
        
        user=authenticate(username=username,password=password) #sujan710 & None
        if user is not None:
            login(request,user) 
            
            if remember_me: 
                request.session.set_expiry(3600)
            else:
                request.session.set_expiry(0)  
            next=request.POST.get('next','') #/menu/
        
            return redirect(next if next else "index")
        else:
            messages.error(request,'password Invalid!!!')
            return redirect('log_in')
            
    next=request.GET.get('next','')   #/about/
        
    return render(request,'accounts/login.html',{'next':next})

def log_out(request):
    logout(request)
    return redirect('log_in')

from django.contrib.auth.forms import PasswordChangeForm

@login_required(login_url='log_in')
def password_change(request):
    form=PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
    return render(request,'accounts/password_change.html',{'form':form})


# pip freeze > requirements.txt
# pip install -r requirements.txt
'''
Deployment 

Domain Name :human readable address of our website 

https://www.sipalaya.com/

https :protcol 
www sub domain
sipalaya -->domain name 
.com -->top level domain



Hosting : renting space on server

shared Hosting : server ()
VPS hosting : (physical server -->virtual server)
Dedicated hosting :amazon 
Cloud (aws,azure):india,

'''
