"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('about/',views.about),
    path('register/',views.register),
    path('login/',views.ulogin),
    path('logout/',views.ulogout),
    path('product_details/<pid>/',views.product_details),
    path('addtocart/<pid>/',views.addtocart),   
    # path('myorder/',views.my_order),
    path('filterbycategory/<cid>/',views.filterbycategory),
    path('sortbyprice/<sid>/',views.sortbyprice),
    path("pricefilter/",views.pricefilter),
    path('cart/',views.viewcart),
    path('deletecart/<pid>/',views.deletecart),
    path('updateqty/<x>/<cid>/',views.updateqty),
    path('order/',views.order),
    path('neworder/',views.neworder),
    path('checkaddress/',views.checkaddress),
    path('placeorder/',views.placeorder),
    path('fetchorder/',views.fetchorder),
    path('makepayment/',views.makepayment),
    path('email_send/',views.email_send),
    path('update_order_status/',views.update_order_status),
    path('myorder/',views.myorder),
    # path('order_history/',views.order_history),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)