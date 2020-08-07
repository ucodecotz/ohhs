from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),
    path('workers_details/<int:pk>/', views.laboursDetails.as_view(), name='details'),
    path('add_comment_to_selected_labour/<int:pk>/', views.add_comment_to_selected_labour, name='add_comment_to_selected_labour'),
    path('Add_to_selected_list/<int:pk>/', views.Add_to_selectedList, name='add_to_selected_list'),
    # path('add_comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', views.Payment.as_view(), name='payment'),

    # path('search/', views.search, name='search'),
]
