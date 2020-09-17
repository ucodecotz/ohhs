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
    path('payment/<payment_option>/', views.PaymentView.as_view(), name='payment'),
    path('myaccount/', views.MyAccount.as_view(), name='myaccount'),
    path('labour_your_Selected/<int:pk>', views.LabourYourSelected, name='labour_your_selected'),
    path('paypal/', views.view_that_asks_for_money, name='paypal'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('request_for_refund/', views.RequestFund.as_view(), name='refund'),
    path('contract/', views.ContractView.as_view(), name='contract'),
    path('contract_view/', views.contract_view, name='contract_view'),
    path('refund_view/', views.refund_view, name='refund_accepted'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    # path('search/', views.search, name='search'),
]
