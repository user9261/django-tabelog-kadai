from django.shortcuts import render

# Create your views here.

from django.contrib.auth import login, authenticate
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .forms import UserEditForm
from django.contrib.auth import get_backends



class SignupView(CreateView):
    """ ユーザー登録用ビュー """
    form_class = SignUpForm # 作成した登録用フォームを設定
    template_name = "accounts/signup.html" 
    success_url = reverse_lazy("login") # ユーザー作成後のリダイレクト先ページ

    def form_valid(self, form):
        response = super().form_valid(form)
        account_id = form.cleaned_data.get("account_id")
        password = form.cleaned_data.get("password1")
        user = authenticate(account_id=account_id, password=password)
        if user:
            # 認証バックエンドを指定
            backend = get_backends()[0]
            user.backend = f'{backend.__module__}.{backend.__class__.__name__}'
            login(self.request, user, backend=user.backend)
        return response



class EditUserView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'accounts/edit_user.html'
    success_url = reverse_lazy('top')

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        # フォームのデータを保存する
        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)