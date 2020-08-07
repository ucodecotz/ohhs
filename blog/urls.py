from django.urls import path
from .views import blog_post_view

urlpatterns = [
    path('blog', blog_post_view, name='blog')
]
