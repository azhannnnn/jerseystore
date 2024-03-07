from django.shortcuts import render,redirect
from .models import *
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.
def home(request):
    data = Products.objects.all()
    return render(request,'index.html',{'data':data})

def products(request):
    data = Products.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 8)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    return render(request,'products.html',{'data':data})

def cart(request):
    return render(request,'cart.html')

def productdetail(request,pk):
    data = Products.objects.get(id=pk)
    data1 = Products.objects.all()
    return render(request,'productdetail.html',{'data':data,'data1':data1})

def account(request):
    return render(request,'account.html')


def register(request):
    if request.method == 'POST':
        name=request.POST.get('rname')
        email=request.POST.get('remail')
        password=request.POST.get('rpassword')
        cpassword=request.POST.get('rcpassword')
        user = Register.objects.filter(Email=email)

        if user:
            message = "User already exist"
            return render(request, "account.html", {"regmsg": message})
        else:
            if password == cpassword:
                Register.objects.create(
                    Username=name,
                    Email=email,
                    Password=password,
                )
                message = "User register Successfully"
                return render(request, "account.html", {"regmsg": message})
            else:
                message = "Password and Confirm Password Does not Match"
                return render(request, "account.html", {"regmsg": message})
            

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        # Checking the emailid with database
        user = Register.objects.filter(Email=email)
        if user:
            data = Register.objects.get(Email=email)
            if data.Password == password:
                id  = data.id
                username = data.Username
                email = data.Email
                password = data.Password
                request.session['id']=id
                request.session['name']=username
                request.session['email']=email
                user={
                    'name':username,
                    'email':email,
                    'password':password,
                }
                # data = Products.objects.filter(Type="tshirt")
                # data1 = Products.objects.filter(Type="shoes")
                # data2 = Products.objects.filter(Type="glasses")
                return render(request,"user.html",{"user":user})
            else:
                message = "Password does not match"
                return render(request,"account.html",{'logmsg':message})
        else:
            message = "User does not exist"
            return render(request,"account.html",{'logmsg':message})            
        
def logout(request):
    
    del request.session['id']
    del request.session['name']
    del request.session['email']
    request.session.flush()

    return redirect('home')        

def cart(request):
    card = request.session['card']
    data = {}
    key = 1
    sum = 0
    items = 0
    for i in card:
        data[key] = Products.objects.get(id=i)
        sum = sum + data[key].Price
        key+=1
    items += len(data.keys())
    sum2 = sum +35
    return render(request,'cart.html', {"data": data.values,'sum':sum,'items':items,'sum2':sum2})

def add_cart(request,pk):
    card = request.session.get('card',[])
    card.append(pk)
    request.session['card'] = card
    print(card)
    data = Products.objects.get(id=pk)
    return render(request,'productDetail.html', {"data": data})
    
def remove(request,pk):
     card = request.session['card']
     card.remove(pk)
     request.session['card'] = card
     return redirect('/cart')


def checkout(request):
    card = request.session['card']
    data = {}
    key = 1
    sum = 0
    items = 0
    for i in card:
        data[key] = Products.objects.get(id=i)
        sum = sum + data[key].Price
        key+=1
    items += len(data.keys())
    username = request.session['name']
    email=request.session['email']
    
    sum = sum+35
    return render(request,'checkout.html',{"data": data.values,'sum':sum,'items':items,'username':username, 'email':email})