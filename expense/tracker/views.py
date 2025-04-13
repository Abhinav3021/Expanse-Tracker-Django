from django.shortcuts import render,redirect
from django.contrib import messages
from tracker.models import Transaction
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def registration(request):
    if(request.method=='POST'):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user_obj= User.objects.filter(
            Q(email=email) | Q(username=username)
        )
        
        if user_obj.exists():
            messages.error(request,'Error: Username or Email already exists')
            return redirect('/registration/')
        
        user_obj=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        messages.error(request,'Success: Account Created')
        return redirect('/registration/')
    
    
    return render(request,'register.html')


def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(
          username = username
            )
        if not user_obj.exists():
            messages.error(request, 'Error: Username does not exist')
            return redirect('/login/')

       # as the password is encrypted , we can't check by (=)....so we need to use authenticate function
        user_obj = authenticate(username = username , password = password) # authenticate will return the object if true

        if not user_obj:
            messages.error(request, 'Error: Invalid credentials')
            return redirect('/login/')
        
        login(request, user_obj) # Genrate the cookie used by django session
        return redirect('/') # redirect to the main page
        

    return render(request , 'login.html')
    

def logout_page(request):
    logout(request)
    messages.error(request,"Success: LogOut Successfull")
    return redirect('/login/')

@login_required(login_url='/login/')  # decorater for protecting the routes
def index(request):
    #print(request.user)
    if(request.method=="POST"):
        description=request.POST.get('description')
        amount=request.POST.get('amount')
        
        print(description,amount)
        if description is "":
            messages.info(request, "Description can not be blank.")
            return redirect('/')
        
        try:
            amount= float(amount)
        except Exception as e:
            messages.info(request, "Amount should be a number.")
            return redirect('/')
        amount=int(amount)
        
        #Holding  the data in the database
        Transaction.objects.create(
            description=description,
            amount=amount,
            created_by=request.user
        )
    
        return redirect('/')
    
    context={'transcations':Transaction.objects.filter(created_by=request.user),
             'balance':Transaction.objects.filter(created_by=request.user).aggregate(total_balance=Sum('amount'))['total_balance'] or 0,
             'income':Transaction.objects.filter(created_by=request.user,amount__gte=0).aggregate(income=Sum('amount'))['income'] or 0,
             'expanse':Transaction.objects.filter(created_by=request.user,amount__lte=0).aggregate(expanse=Sum('amount'))['expanse'] or 0,
             }
    #print(context)
    return render(request,'index.html',context) #In Django, context is a dictionary that contains data you want to pass from your view to your template. This data can then be accessed and displayed in the template.

@login_required(login_url='/login/') 
def deleteTransaction(request,uuid):
    Transaction.objects.get(uuid=uuid).delete()
    return redirect('/')
    