from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from web_app.models import Employees
from django.db.models import Q

# Create your views here.

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True,max_age=0)
def HomePage(request):
    if request.user.is_authenticated:
        name=request.user.first_name
        return render(request,'home.html',{'name': name})
    else:
        messages.error(request,'Please Login')
        return redirect('signin')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True,max_age=0)
def SignUpPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password')
        pass2=request.POST.get('password1')
        
        if User.objects.filter(username=uname):
            messages.error(request,"Username already exists!,Try another username.")
            return redirect('signup')
        if User.objects.filter(email=email):
            messages.error(request,"Email already registered")
            return redirect('signup')

        if pass1!=pass2:
            messages.error(request,"password doesn't match!!")
            return redirect('signup')
        else:
            my_user=User.objects.create_user(uname,email,pass1)

            my_user.save()

            messages.success(request,'Your account has been succesfully created')
            return redirect('login')

    return render(request,'signup.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True,max_age=0)
def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"INVALID USERNAME OR PASSWORD")
            return redirect('login')
    return render (request,'login.html')

def INDEX(request):
    if request.user.is_superuser:

        if request.GET.get('search') is not None:
            search=request.GET.get('search')
            emp = User.objects.filter(
                Q(username__contains=search) | Q(email__contains=search)
            )
            # emp=User.objects.filter(username__contains=search)
        else:
            emp = User.objects.all()
        context = {
            'emp':emp,
        }
        return render(request,'dashboard.html',context)
    else:
        return redirect('home')
    
def ADD(request):
    if request.user.is_superuser:

        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            address= request.POST.get('address')
            phone = request.POST.get('phone')

            emp = User(
                username = name,
                email = email,
                # address = address,
                # phone = phone

            )
            emp.save()
            return redirect('admin')
        return render(request,'dashboard.html') 
    else:
        return redirect('home')
    


def Edit(request):
    emp = User.objects.all()

    context = {
        'emp':emp,
    }
    return redirect(request,'dashboard.html',context)

def Update(request,id):
    if request.user.is_superuser:
        emp=User.objects.get(id=id)

        if request.method =="POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            # address = request.POST.get('address')
            # phone = request.POST.get('phone')


            emp = User(
                id = id,
                username = name,
                email = email,
                # address = address,
                # phone = phone,
            )
            emp.save()
            return redirect('admin')
        return render(request,'dashboard.html')     
    else:
        return redirect('home')

def Delete(request,id):
    emp = User.objects.filter(id =id)
    emp.delete()
    
    context = {
        'emp':emp,
    }
    return redirect('admin')



@cache_control(no_cache=True, must_revalidate=True, no_store=True,max_age=0)
def LogoutPage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged Out Successfully!")
        return redirect('login')