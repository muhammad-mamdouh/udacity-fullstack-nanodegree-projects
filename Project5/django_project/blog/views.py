from django.shortcuts import render


posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'October 6, 2019'
    },
    {
        'author': 'M_Mamdouh',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'October 18, 2019'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
