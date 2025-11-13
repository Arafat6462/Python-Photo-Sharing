from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import models
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
    photos = Photo.objects.annotate(
        average_rating=Avg('ratings__score'),
        rating_count=Count('ratings')
    ).order_by('-id')
    return render(request, 'gallery.html', {'photos': photos})

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    comments = photo.comments.all().order_by('-created_at') # Added this line
    rating_info = photo.ratings.aggregate(average_rating=Avg('score'), rating_count=Count('id'))
    
    comment_form = CommentForm()
    
    # Get user's existing rating to pre-fill the form
    rating_initial_data = {}
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(photo=photo, user=request.user).first()
        if user_rating:
            rating_initial_data['score'] = user_rating.score
            
    rating_form = RatingForm(initial=rating_initial_data)

    context = {
        'photo': photo,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'average_rating': rating_info['average_rating'] or 0,
        'rating_count': rating_info['rating_count'] or 0,
    }
    return render(request, 'photo_detail.html', context)

@login_required
@require_POST
def add_comment(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.photo = photo
        new_comment.user = request.user
        new_comment.save()
        return JsonResponse({
            'success': True,
            'comment': {
                'user': new_comment.user.username,
                'text': new_comment.text,
                'created_at': new_comment.created_at.strftime('%b. %d, %Y, %-I:%M %p')
            }
        })
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def add_rating(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    form = RatingForm(request.POST)
    if form.is_valid():
        Rating.objects.update_or_create(
            photo=photo,
            user=request.user,
            defaults={'score': form.cleaned_data['score']}
        )
        # Recalculate average rating
        rating_info = photo.ratings.aggregate(average_rating=Avg('score'), rating_count=Count('id'))
        return JsonResponse({
            'success': True,
            'average_rating': round(rating_info['average_rating'] or 0, 1),
            'rating_count': rating_info['rating_count'] or 0
        })
    return JsonResponse({'success': False, 'errors': form.errors})