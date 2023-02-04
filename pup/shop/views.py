from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from numpy import product
from .models import Product, category, BusinessUser, CustomUser, Cart
from math import ceil
from django.db.models import Count
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from json import dumps
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import datetime
import json
import requests
import random

# Create your views here.
def index(request):
    
    # resp = requests.get('https://api.unsplash.com/search/photos?query=Nikon&client_id=kkWMO3R7ir8H1fBCKulrOqx5RtHy9BJ-sU7HjSJM0Gk')
    # data = resp.json()
    # number = random.randrange(1,10)
    # url = data['results'][number]['urls']['regular']
    
    Categories = category.objects.all()
    products = Product.objects.all()
    n = len(products)
    nSlides = n//3 + ceil((n/3)-(n//3))
    nc = len(Categories)//2
    Brands = []
    prod = Product.objects.all()
    for x in prod:
        if (x.product_subcategory not in Brands):
            Brands.append(x.product_subcategory)
        else:
            pass
    

    # logic for Cart 
    if request.user.is_authenticated:
        un = request.user.id
        mycart = Cart.objects.filter(user=un)
        myitems = {}
        myprod = {}
        tc = 0  # Product count
        tp = 0  # Total price of the cart. 
        for x in mycart:
            itemslist = x.cart_items.split(",")

        ic = 0
        for y in itemslist:
            for z in itemslist:
                if(y == z):
                    ic = ic+ 1
            myitems.update({y: ic})
            ic = 0

        for x in myitems:
            if(x != 'NA'): 
                myprod.update({Product.objects.filter(product_name__iexact = x): myitems[x]})
        print(myprod)
        for i in myprod.values():
            tc = tc + i
        for i in myprod:
            for z in i:
                tp = tp + z.product_price*myprod[i]
    else: 
        myprod = "NA"
        tc = 0
        tp = 0
    
    params = {'myproducts': products, 'no_of_slides': nSlides, 'range': range((nSlides)), 'Categories': Categories, 'crange': range(nc),
        'myitems': myprod, 'totalcount': tc, 'totalprice': tp, 'Brand': Brands}
    return render(request, 'shop/Home1.html', params)

# def test(request):
#     un = request.user.id
#     CU = CustomUser.objects.filter(user = un)
#     BU = BusinessUser.objects.filter(user = un)
#     print(BU)
#     params = {'un':CU, 'cn': BU}
#     return render(request, 'shop/test.html', params)

def Productviewer(request):
    Categories = category.objects.all()
    Brand_name = request.GET.get('b_name', 'NA')
    products = Product.objects.filter(product_subcategory__icontains = Brand_name)
    p = []
    for x in Categories:
        p.append(products.filter(product_category = x))
    params = {'b_name': Brand_name, 'Prod': p, 'Cat': Categories}
    return render(request, 'shop/Productview.html', params)

def handlesignup(request):
    if(request.method == 'POST'):
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        ph_number = request.POST['phonenumber']
        pass1 = request.POST['password']
        pass2 = request.POST['re-password']
        
        if pass1 != pass2:
            messages.error(request, "Your passwords dont match. ")
            return redirect('Home page')
        if len(ph_number) != 10:
            messages.error(request, "Please enter a valid phone number")
            return redirect('Home page')
        #creating user 
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        customuser = CustomUser(user = myuser, Phone_no = ph_number, DOB = '1111-01-01 01:01')
        customuser.save()
        cart = Cart(user = myuser)
        cart.save()
        messages.success(request, "Your pup account has been succesfully created")
        return redirect('Home page')
    messages.error(request, "Your pup account was not created ")
    return redirect('Home page')
    

def Productpage(request):
    Pd_name = request.GET.get('pname', 'NA')
    cartupdt = request.GET.get('cartupdt', 'NA')
    products = Product.objects.filter(product_name__iexact= Pd_name)
    params = {'Prod': products, 'crtupdt': cartupdt}
    return render(request, 'shop/Productpage.html', params)

def Productviewer2(request):
    c_name = request.GET.get('cname', 'NA')
    Categories = category.objects.filter(cat_name = c_name)
    products = Product.objects.filter(product_category = Categories)
    params = {'Prod': products}
    return render(request, 'shop/Productview2.html', params)

def handlelogin(request):
    if(request.method == 'POST'):
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpassword']

        user = authenticate(username = loginusername, password = loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.first_name}, you are successfully logged in")
            return redirect('Home page')
        else:
            messages.error(request, "Invalid credentials please try again")
            return redirect('Home page')
    return HttpResponse('404 not found')

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('Home page')

def Sellerpage(request):
    un = request.user.id
    CU = CustomUser.objects.filter(user = un)
    BU = BusinessUser.objects.filter(user = un)
    Cat = category.objects.all()
    for x in CU:
        U_seller = x.user_buyer
    User_product = Product.objects.filter(product_seller = un) # Products uploaded by the user
    print(User_product)
    params = {'user': un, 'CU': CU, 'Usp': User_product, 'Buss_user': BU, 'cat': Cat}
    if U_seller == True:
        return render(request, 'shop/Profile.html', params)
    else:
        return render(request, 'shop/Sellerpage.html', params)

def Cartpage(request):
    un = request.user.id
    mycart = Cart.objects.filter(user=un)
    myitems = {}
    myprod = {}
    tc = 0  # Product count
    tp = 0  # Total price of the cart. 
    for x in mycart:
        itemslist = x.cart_items.split(",")
    print(itemslist)
    ic = 0
    for y in itemslist:
        for z in itemslist:
            if(y == z):
                ic = ic+ 1
        myitems.update({y: ic})
        ic = 0

    for x in myitems:
        if(x != 'NA'): 
            myprod.update({Product.objects.filter(product_name__iexact = x): myitems[x]})
    print(myprod)
    for i in myprod.values():
        tc = tc + i
    for i in myprod:
        for z in i:
            tp = tp + z.product_price*myprod[i]
    
    params = {'myitems': myprod, 'totalcount': tc, 'totalprice': tp}
    return render(request, 'shop/cart.html', params)

def Addtocart(request):
    Pd_name = request.GET.get('pn', 'NA')
    myproduct = Product.objects.filter(product_name__iexact= Pd_name)
    un = request.user.id
    mycart = Cart.objects.filter(user = un)
    for y in myproduct:
        productname = y.product_name
    for x in mycart:
        x.cart_items = x.cart_items + ',' + productname
        if(x.save()):
            messages.success(request, "Something went wrong")
            return redirect('/shop/page?pname='+productname)
        else:
            messages.success(request, "Added to cart")
            return redirect('/shop/page?pname='+productname)

def deleteitem(request):
    if(request.method == "POST"):
        updtcount = request.POST.get('quantity')
        prod_name = request.POST.get('prod_name')
    un = request.user.id
    mycart = Cart.objects.filter(user=un)
    listnew = []
    myitems = {}
    ic = 0
    for x in mycart:
        itemslistold = x.cart_items.split(",")
    for y in itemslistold:
        for z in itemslistold:
            if(y == z):
                ic = ic+ 1
        myitems.update({y: ic})
        ic = 0
    myitems[prod_name] = int(updtcount)
    for key in myitems:
        for x in range(myitems[key]):
            listnew.append(key)
    newcart = ",".join(listnew)
    print(type(newcart))
    for x in mycart:
        x.cart_items = newcart
        x.save()
    messages.success(request, "Cart updated successfully")
    return redirect('/shop/cart')

def Productlist(request):
    if (request.method == 'POST'):
        search = request.POST.get('searchtxt')
        try:
            Cat = category.objects.get(cat_name__icontains = search)
            prods = Product.objects.filter(product_category = Cat)
        except ObjectDoesNotExist:
            multiple_q = Q(Q(product_name__icontains = search) | Q(product_subcategory__icontains = search)) 
            prods = Product.objects.filter(multiple_q)
            
        print(prods)
    params = {'prod': prods}
    return render(request, 'shop/productlist.html', params)

def Productentry(request):
    if request.method == "POST":
        name = request.POST.get('name')
        subcat = request.POST.get('subcat')
        desc = request.POST.get('desc')
        amt = request.POST.get('amtavail')
        price = request.POST.get('price')
        cat = request.POST.get('cat')
        newcat = request.POST.get('newcat')
        prodimg = request.FILES.get('image')
        if(cat == 'Not listed'):
            mycat = category(cat_name = newcat)
            mycat.save()
            cat = newcat
        un = request.user.id
        BU = BusinessUser.objects.get(user = un)
        Cat = category.objects.get(cat_name = cat)
        prod = Product(product_name = name, product_category = Cat, product_subcategory = subcat, product_desc = desc, product_price = price, product_seller = BU, product_image = prodimg)
        if prod.save():
            return HttpResponse("product added failed")
        else:
            return redirect('/shop/Sell')