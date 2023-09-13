from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import cache_control
# from django.http import HttpResponse, Http404



# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
   return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminpanel(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'adminpanel.html')
    else:
        return redirect ('/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userlist(request):
    if request.user.is_authenticated and request.user.is_superuser:
        data=User.objects.all()
        context={"data":data}
        return render(request,'userlist.html',context)
    else:
        return redirect ("/")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def handlelogin(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("/adminpanel")
    else :
        if request.user.is_authenticated:
            return redirect("/index")
        
    if request.method=="POST":
        uname=request.POST.get("username")
        passw=request.POST.get("pass")
        myuser=authenticate(username=uname,password=passw)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect("/") 
        else:
            messages.error(request,"Invalid Credentails")
            return redirect("/login")
        
    return render(request,'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def handlesignup(request):
   
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("adminpanel")
    else :
        if request.user.is_authenticated:
            return redirect("index")
    
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("pass1")
        confirmpass=request.POST.get("pass2")
    # print(uname,email,password,confirmpass)
        if password != confirmpass :
            messages.warning(request,"Password is Incorrect")
            return redirect("/signup")
        try:
            if User.objects.filter(username=username).exists():
               messages.info(request,"Username Is Already Taken")
               return redirect("/signup")
        except:
            pass
        
        try:
            if User.objects.get(email=email):
                messages.info(request,"Email Is Already Taken")
                return redirect("/signup")
        except:
            pass
        
        myuser=User.objects.create_user(username,email,password)
        myuser.save()
        messages.success(request,"Sign Up Success Please Login")
        return redirect("/login") 
            
    return render(request,'signup.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect("/")



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def handleadminlogin(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("/adminpanel")
    
    if request.method=="POST":
        adminname=request.POST.get("adminname")
        adminpassw=request.POST.get("adminpass")
        adminuser=authenticate(username=adminname,password=adminpassw)
        if adminuser is not None and adminuser.is_superuser:
            login(request,adminuser)
            messages.success(request,"Login Success")
            return redirect("/adminpanel")
        else:
            messages.error(request,"Invalid Credentails")
            return redirect("/adminlogin")
            
    return render(request,'adminlogin.html')
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def handleadminlogout(request):
     
    # if request.user.is_authenticated and request.user.is_superuser:
        logout(request)
        messages.info(request,"Logout success")
        return redirect("/")
    # else:
        # return redirect('/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adduser(request):
    
    if request.method=="POST":
        
        newuname=request.POST.get("username")
        newemail=request.POST.get("email")
        newpassword=request.POST.get("pass1")
        newconfirmpassword=request.POST.get("pass2")
        print(newuname,newemail,newpassword,newconfirmpassword)
        
        if ' ' in newuname:
            messages.warning(request, "Username cannot contain spaces")
            return redirect('/userlist')
        
        if newpassword != newconfirmpassword:
            messages.warning(request,"Password is incorrect")
            return redirect('/userlist')
        
        try:
            if User.objects.get(username=newuname):
                messages.info(request,"username already exists")
                return redirect('/userlist')
        except:
            pass
        
        try:
            if User.objects.get(email=newemail):
                messages.info(request,"email already exists")
                return redirect('/userlist')
        except:
            pass

        myuser=User.objects.create_user(newuname,newemail,newpassword)
        myuser.save()
        messages.success(request,"user added successfully")
        return redirect('/userlist')
    return render(request,"userlist.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update(request,id):
    
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method=="POST":
            uname=request.POST.get("username")
            email=request.POST.get("email")
            # password=request.POST.get("pass1")

            edit=User.objects.get(id=id)
            edit.username=uname
            edit.email=email
            
            edit.save()
            messages.warning(request,"user updated successfully")
            return redirect('/userlist')
        
        d=User.objects.get(id=id)
        context = {'d': d }
        return render(request,'useredit.html',context)
        
    else:
        return redirect("/adminpanel")
        
    
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def delete(request,id):
    
    if request.user.is_authenticated and request.user.is_superuser:
        data = User.objects.get(id=id)
        data.delete()
        messages.warning(request, "User deleted successfully")
        return redirect("/userlist")
    else:
        return redirect("/adminpanel")
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def handlesearch(request):
    if request.user.is_authenticated and request.user.is_superuser:
        search_query = request.GET.get('search_query')
        if search_query:
            data = User.objects.filter(username__icontains=search_query)
            if data.exists():
                messages.success(request, "User found.")
            else:
                messages.warning(request, "User not found.")
        else:
            data = User.objects.all()
        context = {
            'data': data,
            'search_query': search_query
        }
    
        return render(request, 'userlist.html', context)
    else:
        return redirect("/adminpanel")