from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User     # for default table
from django.contrib.auth import authenticate,login,logout
from .models import Product,Card,Address,Order#,History
import datetime
import re
import random
import razorpay
from django.core.mail import send_mail
# Create your views here.
        
# index page
def index(request):
    context={}
    products=Product.objects.all()
    # print(products)
    context['products']=products
    return render(request,'index.html',context)


def about(request):
    return render(request,'about.html')


# user Registration Page
def register(request):
        context={}
        if request.method == 'POST':
            e = request.POST['uemail']
            u = request.POST['username']
            p = request.POST['upassword']
            rp = request.POST['urepass']
            
            # print(e,u,p,rp)
            if e=="" or u=="" or p=="" or rp=="":
                context['error_msg']="All Fields Are Required"
                return render(request,'register.html',context)
            
            elif p != rp:
                context['error_msg']="Pasword Doesnot Match"
                return render(request,'register.html',context)
            
            elif len(p) <8 or len(rp) <8:
                context['error_msg']="Pasword Contain Atleast 8 Character"
                return render(request,'register.html',context)
            
            else:
                u = User.objects.create(email=e, username=u)
                u.set_password(rp)
                u.save()
                # return HttpResponse("Data Fetched")
                return redirect('/login')
        else:
            return render(request,'register.html')


# user Login Page
def ulogin(request):
    context={}
    if request.method == "POST":
            un = request.POST['uname']
            up = request.POST['upass']

            

            if un == "" or up == "":
                context['error_msg']="All Fields are Required"
                return render(request,'ulogin.html',context)
                 
                # print(un,up)

            else:
                u = authenticate(username = un,password=up)
                # print(u)
                
            
                if u!= None:
                    login(request,u)
                    return redirect('/')
                    
                else:
                    context['error_msg']="Invalid Username Or Password"
                    return render(request,'ulogin.html',context)
                    
    else:
         return render(request,'ulogin.html')


# logout / session expired
def ulogout(request):
    logout(request)
    return redirect('/login')    

def product_details(request,pid):
    context={}
    prod=Product.objects.filter(id=pid)
    context['product']=prod
    return render(request,'product_details.html',context)






def filterbycategory(request, cid):
    context={}
    product=Product.objects.filter(category=cid)
    context['products']= product
    return render (request,"index.html",context)


def sortbyprice(request, sid):
    context={}
    if sid == '0':
        products = Product.objects.order_by('price')
    else:    
        products = Product.objects.order_by('-price')

    context['products'] = products
    return render (request,"index.html",context)
    
def pricefilter(request):
    context={}
    mx=request.GET["max"]
    mn=request.GET["min"]
    q1 = Q(offer_price__gte=mn)
    q2 = Q(offer_price__lte=mx)
    product = Product.objects.filter(q1 & q2)
    context["products"] = product
    return render(request,'index.html',context)




def addtocart(request,pid):

    product=Product.objects.filter(id=pid)
    context={}
    context['product']=product

    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid)
        #print(u[0],p[0]) #user name and product name
        q1=Q(userid=u[0])
        q2=Q(pid=p[0])
        c=Card.objects.filter(q1 & q2)
        if len(c)==1:
            context['error'] = "Product Already in cart"   
            return render(request,'product_details.html',context)
        else:
            card=Card.objects.create(userid=u[0],pid=p[0])
            card.save()
            context['success']="Product Added In Cart"
            return render(request,'product_details.html',context)

            

    else:
        context['error']="Please Login First"
        return render(request,'product_details.html',context)
    


def viewcart(request):
    context={}
    cards=Card.objects.filter(userid=request.user.id)
    saving_amt=0
    total_amt=0
    items=0

    for cart in cards:
        saving_amt += (cart.pid.price - cart.pid.offer_price) * cart.qty
        total_amt += cart.pid.offer_price * cart.qty
        items+=cart.qty

        context['saving']=saving_amt
        context['amount']=total_amt
        context['items']=items

    if len(cards)==0:
        context['msg']="No Items In Cart"
        return render(request,'cart.html',context)
    else:
        context['cart']=cards
        return render(request,'cart.html',context)
    
    
def deletecart(request,pid):
    context={}
    cart=Card.objects.filter(id=pid)
    cart.delete()
    return redirect("/cart")
    
   
#update the product quantity
def updateqty(request,x,cid): # x for value of 0 in cart <a href="/updateqty/0/{{c.id}}/">
    # print('X=',x)
    # print('CID=',cid)

    cart=Card.objects.filter(id=cid)
    quantity = cart[0].qty
    # print(quantity)
    if x =='1':
        quantity+=1
    elif quantity > 1:
        quantity-=1

    cart.update(qty=quantity)             
    return redirect("/cart")


def order(request):
    return render(request,'myorder.html')

def neworder(request):
    return render(request,'placed_order.html')

def checkaddress(request):
    context={}
    u = User.objects.filter(id=request.user.id)
    add = Address.objects.filter(userid = u[0])
    if len(add) >= 1:
        return redirect('/placeorder')
    else:
        if request.method == 'POST':
            fn=request.POST["full_name"]
            ad=request.POST["address"]
            ct=request.POST["city"]
            st=request.POST["state"]
            zp=request.POST["zipcode"]
            mob=request.POST["mobile"]
            if re.match("[6-9]\d{9}",mob):
                obj = Address.objects.create(userid = u[0],fullname=fn,address=ad,city=ct,state=st,pincode=zp,mobile=mob)
                obj.save()
                return redirect('/placeorder')
                # return HttpResponse(fn+ad+ct+st+zp+mob) 
            else:
                context["error_msg"] = "Warning : Incorrect Mobile Number Please Enter Valid Mobile Number"
                return render(request,'address.html',context)

        else:
            return render(request,'address.html')


def placeorder(request):
    carts=Card.objects.filter(userid=request.user.id)
    for i in carts:
        oid = random.randint(1111,9999)
        totalamt = i.pid.offer_price*i.qty

        order = Order.objects.create(order_id=oid,user_id=i.userid,p_id=i.pid,amt=totalamt,qty=i.qty)
        order.save()
    # carts.delete()    
    return redirect('/fetchorder')



def fetchorder(request):
    context={}
    u = User.objects.filter(id=request.user.id) # for current user\
    carts=Card.objects.filter(userid=request.user.id)
    address = Address.objects.filter(userid = u[0])
    q1=Q(user_id=u[0])
    q2=Q(payment_status="unpaid")   # for payment status
    orders = Order.objects.filter(q1&q2)
    context['address']=address
    context['order']=orders
    

    cards=Card.objects.filter(userid=request.user.id)
    saving_amt=0
    total_amt=0
    items=0


    for cart in cards:
        saving_amt += (cart.pid.price - cart.pid.offer_price) * cart.qty
        total_amt += cart.pid.offer_price * cart.qty
        items+=cart.qty
        amount = saving_amt + total_amt

    # for i in orders:
    #     total_amt+=i.amt
    #     items+=i.qty
    #     saving_amt += (i.price - i.offer_price) * i.qty

        context['saving']=saving_amt
        context['amount']=total_amt
        context['items']=items
        context['finalamount']=amount
        
    return render(request,'placeorder.html',context)

def makepayment(request):
    context={}

    cards=Card.objects.filter(userid=request.user.id)
    saving_amt=0
    total_amt=0
    items=0

    for cart in cards:
        saving_amt += (cart.pid.price - cart.pid.offer_price) * cart.qty
        total_amt += cart.pid.offer_price * cart.qty
        items+=cart.qty
        amount = saving_amt + total_amt

        context['saving']=saving_amt
        context['finalamount']=amount
        context['amount']=total_amt
        context['items']=items

        
    u=User.objects.filter(id=request.user.id)
    # orders=Order.objects.filter(user_id=u[0])
    q1=Q(user_id=u[0])
    q2=Q(payment_status="unpaid")       # for payment status
    orders = Order.objects.filter(q1&q2)

    sum=0

    for order in orders:
        sum+=order.amt
        orderid=order.order_id

    for user in u:
        name = user.username
        email = user.email

    client = razorpay.Client(auth=("rzp_test_2zJjEbeRT0fAQQ","4tEfDY2fzqhAENnHpl7S03L2"))
    data = {"amount":sum*100, "currency":"INR", "receipt":orderid}
    payment = client.order.create(data=data)
    context['payment']=payment
    context['order']=orders
    return render(request,'pay.html',context)


def email_send(request):
    send_mail(
        "EasyMart Order Confirmation",
        "Your Order Is Confirm \n Thank You",
        "ashitosh.rohom@gmail.com",
        ['ashitoshrohom1829@gmail.com'],
        )
    return redirect('/myorder')
    # return redirect('/update_order_status')



def update_order_status(request):
    context={}
    u=User.objects.filter(id=request.user.id)
    q1=Q(user_id=u[0])
    q2=Q(payment_status="unpaid")       # for payment status
    orders = Order.objects.filter(q1&q2)
    orders.update(payment_status="Paid")

    # return HttpResponse("Order Status Changed")
    return redirect('/')



# def order_history(request):
#     user=User.objects.filter(id=request.user.id)
#     orders=Order.objects.filter(user_id=user[0])
#     addr=Address.objects.filter(userid=user[0])
#     a=""
#     for x in addr:
#         a+=x.fullname + "" + x.address + "" + x.city + "" + x.state + "" + x.pincode

#     for i in orders:
#         myorder=History.objects.create(order_id=orders[0], userid=user[0], amount=i.amt, address=a, status="Delivered")
#         myorder.save()
#     # return redirect('/')
#     return HttpResponse("Your History Created !")

def myorder(request):
    context={}
    data = Order.objects.filter(user_id=request.user.id)
    context['order']=data
    return render(request,'myorder.html',context)