from django.shortcuts import render
from .models import BlogPost


# Create your views here.

def blog_post_view(request):
    post_query_set = BlogPost.objects.all()
    context = {
        'blog_list':post_query_set
    }
    return render(request,'blog.html', context )
