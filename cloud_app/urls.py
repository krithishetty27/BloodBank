from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('diagnosis/', views.diagnosis , name='diagnosis'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('profile/', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('payment/<int:appointment_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment/dummy/<int:payment_id>/', views.dummy_payment, name='dummy_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
