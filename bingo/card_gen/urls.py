"""
URL configuration for bingo project.

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
from django.urls import path, include
from card_gen import views
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('card-create/', views.card_create, name='card_create'),
    path('generate-bingo-cards/', views.generate_bingo_cards, name='generate_bingo_cards'),
    path('', views.home, name='home'),
    path('home/',views.home,name='home'),
    path('api/generate-bingo-cards/', views.generate_bingo_cards, name='generate_bingo_cards'),
    path('call-number/', views.call_numbers, name='call_number'),
    path('api/call-number/', views.call_number, name='call_number'),
    path('api/reset-called-numbers/', views.reset_called_numbers, name='reset_called_numbers'),
    path('card/<str:serial_number>/', views.view_bingo_card, name='view_bingo_card'),
    path('api/mark_number/<str:serial_number>/', views.mark_number, name='mark_number'),
    path('verify-bingo-claim/', views.verify, name='verify'),
    path('verify-bingo-claim/<int:serial_number>/', views.view_mark_bingo_card, name='view_mark_bingo_card'),
    path('api/bingo-cards/<int:serial_number>/', views.bingo_card_api, name='bingo_card_api'),
]
