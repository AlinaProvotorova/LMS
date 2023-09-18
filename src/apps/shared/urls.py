from django.urls import path

from .views import index, documents, support, payment, about_us

urlpatterns = [
    path('', index, name='index'),
    path('documents-university', documents, name='documents_university'),
    path('support', support, name='support'),
    path('payment', payment, name='payment'),
    path('about_us', about_us, name='about_us'),
]
