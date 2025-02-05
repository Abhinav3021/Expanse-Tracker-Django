from django.shortcuts import render,redirect
from django.contrib import messages
from tracker.models import Transaction
from django.db.models import Sum

# Create your views here.
def index(request):
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
        )
    
        return redirect('/')
    
    context={'transcations':Transaction.objects.all(),
             'balance':Transaction.objects.all().aggregate(total_balance=Sum('amount'))['total_balance'] or 0,
             'income':Transaction.objects.filter(amount__gte=0).aggregate(income=Sum('amount'))['income'] or 0,
             'expanse':Transaction.objects.filter(amount__lte=0).aggregate(expanse=Sum('amount'))['expanse'] or 0,
             }
    #print(context)
    return render(request,'index.html',context) #In Django, context is a dictionary that contains data you want to pass from your view to your template. This data can then be accessed and displayed in the template.

def deleteTransaction(request,uuid):
    Transaction.objects.get(uuid=uuid).delete()
    return redirect('/')
    