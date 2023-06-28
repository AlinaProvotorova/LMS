from django.urls import path

from .views import index, documents

urlpatterns = [
    path('', index, name='index'),
    path('documents-university', documents, name='documents_university'),
]
