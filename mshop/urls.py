"""mshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from shop.views import index, product, cart, add_to_cart, remove_from_cart, order, my_orders, payment, payment_done, \
    payment_canceled

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', index),
    # path('<int:cat_id>', index),
    url(r'^(\d*)$', index),
    path('accounts/', include('allauth.urls')),
    url(r'filer/', include('filer.urls')),
    path('product/<int:product_id>/', product, name='product-url'),
    path('cart/', cart),
    path('additem/<int:product_id>/<int:quantity>/', add_to_cart, name='additem-url'),
    path('removeitem/<int:product_id>/', remove_from_cart, name='removeitem-url'),
    path('order/', order),
    path('myorders/', my_orders),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment/<int:order_id>/', payment),
    path('done/', payment_done),
    path('canceled/', payment_canceled),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
