from django.shortcuts import render
from django.conf import settings
from django.views.generic import TemplateView, ListView, DetailView
from .models import Restaurant
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect

from django.shortcuts import redirect
from django.contrib import messages


import stripe
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

from .models import Subscription


class TopView(TemplateView):
     template_name = "top.html"
     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          user = self.request.user
          if user.is_authenticated:
               context['has_subscription'] = Subscription.objects.filter(user=user).exists()
          else:
               context['has_subscription'] = False
          return context
     
     
class RestaurantListView(ListView):
     model = Restaurant
     template_name = "top.html"
      

class RestaurantDetailView(DetailView):
    model = Restaurant 
    context_object_name = "Restaurant_detail"
    template_name = "crud/Restaurant_detail.html"


      
class LoginView(LoginView):
     form_class = AuthenticationForm
     template_name = 'login.html'
 
class LogoutView(LoginRequiredMixin, LogoutView):
     template_name = 'top.html'

class PaymentFormView(TemplateView):
     template_name = 'payment_form.html'

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        return context
     

@method_decorator(csrf_exempt, name='dispatch')
class CreateSubscriptionView(View):

    def post(self, request, *args, **kwargs):
        token = request.POST.get('stripeToken')
        price_id = 'price_1P5IspGbmPUm5RpaXdJhHLsG'

        try:
            customer = stripe.Customer.create(
                source=token,
                email=request.user.email
            )
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{'price': price_id}],
            )

            django_subscription = Subscription(
                user=request.user,
                stripe_subscription_id=subscription.id,
                stripe_customer_id=customer.id
            )
            django_subscription.save()

            messages.success(request, 'Subscription created successfully!')
            return redirect('top')
        except stripe.error.StripeError as e:
            print(f'Error creating subscription: {str(e)}')
            messages.error(request, f'Error creating subscription: {str(e)}')
            return redirect('top')

class CustomerPortalView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY


        # Stripeの顧客IDを取得（実際にはユーザーモデル等から取得する）
        user = request.user,
        customer_id = Subscription.objects.get(user=user).stripe_customer_id

        # 顧客ポータルセッションの作成
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url="http://127.0.0.1:8000/",
        )

        # 顧客ポータルのURLへリダイレクト
        return HttpResponseRedirect(session.url)

