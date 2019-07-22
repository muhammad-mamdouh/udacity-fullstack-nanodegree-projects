from django.shortcuts import render
from django.views.generic import ListView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'    # Default naming convention <app>/<modelname>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
