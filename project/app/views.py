from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import razorpay
from django.views.decorators.csrf import csrf_exempt

#===============================================================================================#

# Dashboard pages -> Before Login
def home(request):
    data = Products.objects.all()
    return render(request,'index.html',{'data':data})

# Dashboard pages -> After Login
def user(request):
    data = Products.objects.all()
    return render(request,'user.html',{'data':data})

#===============================================================================================#

# Product Pages
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

def productdetail(request,pk):
    data = Products.objects.get(id=pk)
    data1 = Products.objects.all()
    return render(request,'productdetail.html',{'data':data,'data1':data1})

#===============================================================================================#

# Account Pages -> Registration
def registerpage(request):
    return render(request,'register.html')

def register(request):
    if request.method == 'POST':
        name=request.POST.get('rname')
        email=request.POST.get('remail')
        password=request.POST.get('rpassword')
        cpassword=request.POST.get('rcpassword')
        print(name,email,password)
        user = Register.objects.filter(Email=email)
        if user:
            print("1")
            message = "User already exist"
            return render(request, "login.html", {"regmsg": message})
        else:
            if password == cpassword:
                Register.objects.create(
                    Username=name,
                    Email=email,
                    Password=password,
                )
                message = "User register Successfully"
                return render(request, "login.html", {"regmsg": message})
            else:
                message = "Password and Confirm Password Does not Match"
                return render(request, "register.html", {"regmsg": message})
            

# Account Pages -> Login    

def loginpage(request):
    return render(request,'login.html')            
            

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
                data = Products.objects.all()
                return render(request,"user.html",{"user":user,'data':data})
            else:
                message = "Password does not match"
                return render(request,"login.html",{'logmsg':message})
        else:
            message = "User does not exist"
            return render(request,"register.html",{'logmsg':message})               

# Account Pages -> Logout

def logout(request):
    
    del request.session['id']
    del request.session['name']
    del request.session['email']
    request.session.flush()

    return redirect('home')        

# Account Pages -> My Account

def account(request):
    try:
        name = request.session['name']
        email = request.session['email']
        user = {
            'username':name,
            'email':email
        }
        return render(request,'account.html',user)
    except:
        return render(request,'account.html',{'msg':"Please Login First!!"})

#===============================================================================================#    
    
# Cart Pages -> Cart
        
def cart(request):
    try :
        card = request.session['card']
        
        if card == []:
            
            data = Products.objects.all()
            return render(request,'cart.html',{'msg':"Your Cart is empty, Add Some!",'data':data})
        else:
            data = {}
            key = 1
            sum = 0
            items = 0
            for i in card:
                data[key] = Products.objects.get(id=i)
                sum = sum + data[key].Price
                key+=1
            items += len(data.keys())
            sum2 = sum + 35
            return render(request,'cart.html', {"data": data.values,'sum':sum,'items':items,'sum2':sum2})
    except Exception:
        data = Products.objects.all()
        return render(request,'cart.html',{'msg':"Your Cart is empty, Add Some!",'data':data})

# Cart Pages -> Add to Cart
    
def add_cart(request,pk):
    try:
        name = request.session['name']
        card = request.session.get('card',[])
        card.append(pk)
        request.session['card'] = card
        print(card)
        data = Products.objects.get(id=pk)
        return render(request,'productDetail.html', {"data": data})
    except:
        return redirect('loginpage')

# Cart Pages -> Remove cart
        
def remove(request,pk):
     
     card = request.session['card']
     card.remove(pk)
     request.session['card'] = card
     
     return redirect('/cart')

#===============================================================================================#

# Checkout Pages

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
    
    sum = sum + 35
    return render(request,'checkout.html',{"data": data.values,'sum':sum,'items':items,'username':username, 'email':email})


#===============================================================================================#

# Payment Gateway

def payment(request):
    if request.method=="POST":
        name = request.POST.get('name')
        amount = float(request.POST.get('amount')) * 100
        
        
        client = razorpay.Client(auth=("rzp_test_AcIEh6rX45zRp8","alxj2MIEOtVrhPpGGbMyFvmX"))
        create_payment = client.order.create({'amount':amount, 'currency':'INR','payment_capture':'1' })
        payment = Payment(Name=name, Amount=amount, Payment_id=create_payment['id'])
        payment.save()
        print(create_payment)
        
        return render(request,'checkout.html',{'payment':create_payment})
    

@csrf_exempt
def success(request):
    if request.method=="POST":
        a = request.POST
        print(a)
        return render(request,'success.html')    