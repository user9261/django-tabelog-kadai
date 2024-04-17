"""
URL configuration for kadai_002 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from crud import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.TopView.as_view(), name="top"),
    path('crud/', views.RestaurantListView.as_view(), name="list"),
    path('account', views.TopView.as_view(), name="account"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('payment/', views.PaymentFormView.as_view(), name='payment_form'),
    path('create-subscription/', views.CreateSubscriptionView.as_view(), name='create_subscription'),
    path('billing-portal/', views.CustomerPortalView.as_view(), name='billing-portal'),
    path('crud/detail/<int:pk>', views.RestaurantDetailView.as_view(), name="detail"),
   

]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)