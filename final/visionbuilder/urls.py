from django.urls import path

from . import views

urlpatterns = [
    path('pages/', views.PageListCreate.as_view(), name='pages_list_create'),
    path('pages/<int:pk>/', views.PageRetrieveUpdate.as_view(), name='page_retrieve_update'),
    path('public-pages/', views.PublicPages.as_view(), name='public_pages'),
    path('public-pages/<int:pk>/', views.PublicPagesCode.as_view(), name='public_pages'),
]