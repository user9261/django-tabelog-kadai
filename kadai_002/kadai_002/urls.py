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
from crud import views as crud_views
from accounts import views as accounts_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', crud_views.TopView.as_view(), name="top"),
    path('crud/',crud_views.RestaurantListView.as_view(), name="list"),
    path('account', crud_views.TopView.as_view(), name="account"),
    path('login/', crud_views.LoginView.as_view(), name="login"),
    path('logout/', crud_views.LogoutView.as_view(), name="logout"),
    path('payment/', crud_views.PaymentFormView.as_view(), name='payment_form'),
    path('create-subscription/', crud_views.CreateSubscriptionView.as_view(), name='create_subscription'),
    path('billing-portal/', crud_views.CustomerPortalView.as_view(), name='billing-portal'),
    path('crud/detail/<int:pk>', crud_views.RestaurantDetailView.as_view(), name="detail"),
    path('restaurant/<int:restaurant_id>/review/', crud_views.ReviewView.as_view(), name='review_form'),
    path('mypage/', crud_views.MypageView.as_view(), name='mypage'),
    path('accounts/signup/', accounts_views.SignupView.as_view(), name="signup"),
    path('restaurant/<int:restaurant_id>/toggle_favorite/', crud_views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
    path('restaurant/<int:pk>/', crud_views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('restaurant/<int:restaurant_id>/reserve/', crud_views.CreateReservationView.as_view(), name='create_reservation'),
    path('restaurant/<int:restaurant_id>/cancel/', crud_views.CancelReservationView.as_view(), name='cancel_reservation'),
    
    



]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)