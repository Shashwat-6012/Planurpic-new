from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name = "Home page"),
    # path("test", views.test, name = "Test page"),
    path("PV", views.Productviewer, name = "Product view"),
    path("signup", views.handlesignup, name = "signup"),
    path("page", views.Productpage, name = 'Product page'),
    path("PV2", views.Productviewer2, name = 'Product'),
    path("login", views.handlelogin, name = "login"),
    path("logout", views.handlelogout, name = "logout"),
    path("Sell", views.Sellerpage, name = "Seller"),
    path("cart", views.Cartpage, name = 'Cart'), # redirect to Cart frontend. 
    path("Atc", views.Addtocart, name = "Addtocart"), # redirects to Add to cart view 
    path("Di", views.deleteitem, name = "Deleteincart"),
    path("Pl", views.Productlist, name = "Productlist"),
    path("PE", views.Productentry, name = "productentry") #logic for product entry in DB. 
]