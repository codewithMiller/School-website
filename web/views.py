from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import (
    Staff, SchoolClass, News, Event, GalleryImage,Sponsor
)
from .forms import ApplicationForm, ContactForm


def home(request):
    context = {
        'latest_news': News.objects.filter(published=True)[:3],
        'upcoming_events': Event.objects.filter(date__gte=timezone.now().date())[:4],
        'classes': SchoolClass.objects.all(),
    }
    return render(request, 'web/home.html', context)


def about(request):
    return render(request, 'web/about.html')


def academics(request):
    return render(request, 'web/academics.html', {'classes': SchoolClass.objects.all()})


def admissions(request):
    return render(request, 'web/admissions.html')


def apply(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('apply_success')
    else:
        form = ApplicationForm()
    return render(request, 'web/apply.html', {'form': form})


def apply_success(request):
    return render(request, 'web/apply_success.html')


def news_list(request):
    return render(request, 'web/news_list.html', {
        'news': News.objects.filter(published=True),
    })


def news_detail(request, pk):
    item = get_object_or_404(News, pk=pk, published=True)
    return render(request, 'web/news_details.html', {'item': item})


def gallery(request):
    return render(request, 'web/gallery.html', {'images': GalleryImage.objects.all()})


def staff(request):
    return render(request, 'web/staff.html', {'staff_list': Staff.objects.all()})

def staff_detail(request, pk):
    member = get_object_or_404(Staff, pk=pk)
    return render(request, 'web/staff_detail.html', {'member': member})

def class_details(request, slug_text):
    school_class = get_object_or_404(SchoolClass, slug=slug_text)
    return render(request, 'web/class_details.html', {'class': school_class})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you. We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'web/contact.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome Back!')
            return redirect(request.GET.get('next') or 'home')
        messages.error(request, 'Wrong username or password.')

    return render(request, 'web/login.html')


@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')

def sponsors_view(request):
    sponsor = Sponsor.objects.all()
    return render(request,'web/sponsors.html',{'sponsors':sponsor})