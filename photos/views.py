from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import models # Import the models module
from django.db.models import Avg, Count
from .forms import CustomUserCreationForm, PhotoUploadForm, CommentForm, RatingForm
from .models import Photo, Comment, Rating

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
    photos = Photo.objects.all().order_by('-id')
    return render(request, 'gallery.html', {'photos': photos})

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    comments = photo.comments.all().order_by('-created_at')
    
    # Rating calculation
    rating_info = photo.ratings.aggregate(average_rating=Avg('score'), rating_count=models.Count('score'))
    
    comment_form = CommentForm()
    rating_form = RatingForm()

    if request.method == 'POST' and request.user.is_authenticated:
        # Differentiate between comment and rating form submissions
        if 'submit_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.photo = photo
                new_comment.user = request.user
                new_comment.save()
                return redirect('photo_detail', photo_id=photo.id)
        
        elif 'submit_rating' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                # Update or create rating
                Rating.objects.update_or_create(
                    photo=photo,
                    user=request.user,
                    defaults={'score': rating_form.cleaned_data['score']}
                )
                return redirect('photo_detail', photo_id=photo.id)

    context = {
        'photo': photo,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'average_rating': rating_info['average_rating'] or 0,
        'rating_count': rating_info['rating_count'] or 0,
    }
    return render(request, 'photo_detail.html', context)
