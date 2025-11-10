from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, PhotoUploadForm
from .models import Photo

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('gallery')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def upload_photo(request):
    if not request.user.is_creator:
        return redirect('gallery')
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.creator = request.user
            photo.save()
            return redirect('gallery')
    else:
        form = PhotoUploadForm()
    return render(request, 'upload_photo.html', {'form': form})

def gallery(request):
    photos = Photo.objects.all()
    return render(request, 'gallery.html', {'photos': photos})
