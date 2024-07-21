from django.contrib.auth.views import LoginView, PasswordResetView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from config.settings import EMAIL_HOST_USER
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
import secrets
from users.forms import UserRegisterForm, UserProfileForm, UserLoginForm, UserRecoveryForm
from users.models import User, Payments
import random
import string

from users.serializers import UserSerializer, PaymentsSerializer


def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}/'
        send_mail(
            subject='Email confirmation',
            message=f'Hello! Click on the link to confirm your email: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserLoginView(LoginView):
    model = User
    form_class = UserLoginForm
    # redirect_authenticated_user = True
    success_url = reverse_lazy('catalog:home')


class UserPasswordResetView(PasswordResetView):
    form_class = UserRecoveryForm
    template_name = 'users/recovery_form.html'

    def form_valid(self, form):
        user_email = self.request.POST.get('email')
        user = get_object_or_404(User, email=user_email)
        new_password = generate_random_password()
        user.set_password(new_password)
        user.save()
        send_mail(
            subject="Восстановление пароля",
            message=f"Здравствуйте! Ваш пароль для доступа на наш сайт изменен:\n"
                    f"Данные для входа:\n"
                    f"Email: {user_email}\n"
                    f"Пароль: {new_password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return redirect('users:login')


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_lesson', 'paid_course', 'pay_transfer',)
    ordering_fields = ['pay_date',]


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRegisterView(CreateAPIView):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()


class UserRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class UserUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
