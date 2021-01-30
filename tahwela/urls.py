"""tahwela URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from accounts.views import CreateUserview, LoginView, ConnectBankAccount, UploadMoney, CheckBalance, CurrencyExchange, SendMoney

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('create_user/', CreateUserview.as_view(), name='create'),
    path('login/', LoginView.as_view(), name='login'),
    path('connect_account/', ConnectBankAccount.as_view(), name='connect'),
    path('upload_money/', UploadMoney.as_view(), name='upload'),
    path('check_balance/', CheckBalance.as_view(), name='balance'),
    path('currency/', CurrencyExchange.as_view(), name='currency'),
    path('send_money/', SendMoney.as_view(), name='send_money'),

]
