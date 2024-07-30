from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .news_api import get_news

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'news/login.html', {'form': form})

@login_required
def home(request):
    country = request.GET.get('country', 'us')
    category = request.GET.get('category', 'general')
    page = int(request.GET.get('page', 1))
    
    news = get_news(country=country, category=category, page=page)
    articles = news.get('articles', [])

    return render(request, 'news/home.html', {
        'news': articles,
        'country': country,
        'category': category,
        'page': page,
        'has_more': len(articles) == 20  # True if there might be more articles
    })

def custom_404(request, exception):
    return render(request, 'news/404.html', status=404)