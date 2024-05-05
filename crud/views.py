from django.shortcuts import render
from django.conf import settings
from django.views.generic import TemplateView, ListView, DetailView
from .models import Restaurant, Favorite, Reservation,Review
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages


import stripe
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

from .models import Subscription

class TopView(TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['has_subscription'] = Subscription.objects.filter(user=user).exists()
        else:
            context['has_subscription'] = False
        
        # 検索クエリを取得
        query = self.request.GET.get('search_query')
        if query:
            context['object_list'] = Restaurant.objects.filter(name__icontains=query)
            return context
        else:
            context['object_list'] = Restaurant.objects.all()
        
        # カテゴリーを取得
        category = self.request.GET.get('search_category')
        if category:
            context['object_list'] = Restaurant.objects.filter(category__name__icontains=category)
        else:
            context['object_list'] = Restaurant.objects.all()

        return context


     
     
class RestaurantListView(ListView):
     model = Restaurant
     template_name = "index.html"
      

# crud/views.py

class RestaurantDetailView(LoginRequiredMixin, DetailView):
    model = Restaurant
    template_name = "crud/Restaurant_detail.html"
    context_object_name = "restaurant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = context["restaurant"]
        user = self.request.user
        if user.is_authenticated:
            context["is_favorite"] = Favorite.objects.filter(
                user=user, restaurant=restaurant
            ).exists()
            # 予約の存在チェックを追加
            context["has_reservation"] = Reservation.objects.filter(
                user=user, restaurant=restaurant
            ).exists()

            if context["has_reservation"]:
                context["url"] = "cancel_reservation"
            else:
                context["url"] = "create_reservation"
        else:
            context["is_favorite"] = False
            context["has_reservation"] = False

        # レストランに紐づくレビュー一覧を取得
        context["reviews"] = Review.objects.filter(restaurant=restaurant)
        return context


      
class LoginView(LoginView):
     form_class = AuthenticationForm
     template_name = 'login.html'
 
class LogoutView(LoginRequiredMixin, LogoutView):
     template_name = 'index.html'

class PaymentFormView(TemplateView):
     template_name = 'payment_form.html'

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        user = self.request.user
        context["has_subscription"] = Subscription.objects.filter(user=user).exists()
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

        user = request.user
        try:
            subscription = Subscription.objects.get(user=user)
            customer_id = subscription.stripe_customer_id

            # 顧客ポータルセッションの作成
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url="https://test052214-27c4362284fb.herokuapp.com/",
            )

            # 顧客ポータルのURLへリダイレクト
            return HttpResponseRedirect(session.url)
        except Subscription.DoesNotExist:
            messages.error(request, "有料登録してください。")
            return redirect("top")

    
class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, restaurant_id):

        user = request.user
        if not Subscription.objects.filter(user=user).exists():
            messages.success(request, "有料会員になる必要があります。")
            return redirect("payment_form")

        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)

        if not created:
            favorite.delete()
        else:
            favorite.save()

        return redirect('restaurant_detail', pk=restaurant.id)
    
class CreateReservationView(LoginRequiredMixin, View):
    def post(self, request, restaurant_id):

        user = request.user
        if not Subscription.objects.filter(user=user).exists():
            messages.success(request, "有料会員になる必要があります。")
            return redirect("payment_form")

        user = request.user
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        reservation_date = request.POST.get('reservation_date')
        reservation_time = request.POST.get('reservation_time')
        number_of_people = request.POST.get('number_of_people')

        reservation = Reservation(
            user=user,
            restaurant=restaurant,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
            number_of_people=number_of_people
        )
        reservation.save()

        messages.success(request, "予約が完了しました。")
        return redirect('restaurant_detail', pk=restaurant.id)
    
class CancelReservationView(LoginRequiredMixin, View):
    def post(self, request, restaurant_id):
        user = request.user
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

        user = request.user
        if not Subscription.objects.filter(user=user).exists():
            messages.success(request, "有料会員になる必要があります。")
            return redirect("payment_form")

        reservation = Reservation.objects.filter(user=user, restaurant=restaurant)
        reservation.delete()

        messages.success(request, "予約をキャンセルしました。")
        return redirect('restaurant_detail', pk=restaurant.id)


class ReviewView(TemplateView):
    template_name = "crud/review_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant_id = self.kwargs.get("restaurant_id")
        context["restaurant"] = get_object_or_404(Restaurant, pk=restaurant_id)
        return context

    def post(self, request, restaurant_id):
        user = request.user
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        score = request.POST.get("score", 0)
        comment = request.POST.get("comment", "")
        review = Review(user=user, restaurant=restaurant, score=score, content=comment)
        review.save()

        messages.success(request, "投稿しました。")
        return redirect("restaurant_detail", pk=restaurant.id)
    

class DeleteReviewView(LoginRequiredMixin, View):
    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.user:
            review.delete()
            messages.success(request, "レビューが削除されました。")
        else:
            messages.error(request, "このレビューを削除する権限がありません。")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "top"))



class MypageView(TemplateView):
    template_name = 'mypage.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["has_subscription"] = Subscription.objects.filter(user=user).exists()
        return context

from django.http import JsonResponse
class CancelSubscriptionView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect("login")

        try:
            subscription = Subscription.objects.get(user=user)
            stripe.Subscription.delete(subscription.stripe_subscription_id)
            subscription.delete()
            messages.success(request, "解約が完了しました")
            return redirect("top")
        except Subscription.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "No subscription found."}
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


class FavoritesListView(ListView):
    model = Favorite
    template_name = "favorites_list.html"
    context_object_name = "favorites"

    def get_queryset(self):
        # ログインしているユーザーのお気に入りとそれに紐づいているレストランを取得
        return Favorite.objects.filter(user=self.request.user).select_related('restaurant')

   
class ReservationsListView(ListView):
    model = Reservation
    template_name = "reservations_list.html"
    context_object_name = "reservations"

    def get_queryset(self):
        # ログインしているユーザーの予約のみを取得
        return Reservation.objects.filter(user=self.request.user)


class EditReviewView(DetailView):
    model = Review
    template_name = 'crud/edit_review.html'
    pk_url_kwarg = 'review_id'

    def post(self, request, *args, **kwargs):
        user = request.user
        if not Subscription.objects.filter(user=user).exists():
            messages.success(request, "有料会員になる必要があります。")
            return redirect("payment_form")

        review = self.get_object()
        score = request.POST.get("score")
        content = request.POST.get("content")
        review.score = score
        review.content = content
        review.save()
        return redirect("top")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = self.get_object()
        return context
    
        
    

