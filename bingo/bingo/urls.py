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

admin.site.site_header = "Bingo Administration"
admin.site.site_title = "Bingo Admin Page"
admin.site.index_title = "Welcome to Bingo Admin Page"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('card_gen.urls')),
    path('home/',include('card_gen.urls')),
    path('card-create/',include('card_gen.urls')),
    path('api/generate-bingo-cards/', include('card_gen.urls')),
    path('api/call-number/', include('card_gen.urls')),
    path('api/reset-called-numbers/', include('card_gen.urls')),
    path('view_bingo_card/', include('card_gen.urls')),
    path('api/mark_number/<str:serial_number>/', include ('card_gen.urls')),
    path('verify-bingo-claim/',include('card_gen.urls')),
    path('verify-bingo-claim/<str:serial_number>/',include('card_gen.urls')),
]
