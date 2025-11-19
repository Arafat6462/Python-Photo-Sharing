from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseForbidden
from django.db import models
from django.db.models import Avg, Count
from django.contrib import messages # Import messages for user feedback
from django.views.decorators.cache import cache_page # Import cache_page
from django.core.cache import cache # Import cache
from .forms import CustomUserCreationForm, PhotoUploadForm, CommentForm, RatingForm
from .models import Photo, Comment, Rating

# Utility function to generate a consistent color based on username
def get_user_avatar_color(username):
    # Simple hash function to generate a consistent number from the username
    hash_value = sum(ord(char) for char in username)

    # Generate HSL values for a wide range of colors
    # Hue: Varies across the color spectrum (0-360)
    # Saturation: Kept moderate for a "premium" look (e.g., 50-70%)
    # Lightness: Kept in a mid-range for good contrast (e.g., 40-60%)
    hue = hash_value % 360
    saturation = 60 + (hash_value % 10) # Slightly vary saturation
    lightness = 50 + (hash_value % 10) # Slightly vary lightness

    # Convert HSL to Hexadecimal
    # This is a simplified conversion for CSS HSL, not a full HSL to RGB to Hex
    # For a true "premium" look, we'll use a more controlled set of colors
    # or a more robust HSL to RGB conversion.
    # For now, let's use a more curated list of "premium" colors
    # and pick one based on the hash.

    premium_colors = [
        "#6C7A89", "#967AA1", "#A3BAC3", "#C1946A", "#7E8A97", "#B0A295",
        "#8D99AE", "#A7BED3", "#C5D8E4", "#E0BBE4", "#957DAD", "#D291BC",
        "#FFC72C", "#DA2C38", "#007EA7", "#00A8E8", "#8D6A9F", "#C7B8EA",
        "#84DCC6", "#A8DADC", "#C4F0C5", "#E6F9AF", "#FFD166", "#FCA3B7"
    ]
    return premium_colors[hash_value % len(premium_colors)]

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
            
            # Check the file type and set it
            uploaded_file = request.FILES.get('image')
            if uploaded_file:
                content_type = uploaded_file.content_type
                if content_type.startswith('video'):
                    photo.file_type = 'video'
                else:
                    photo.file_type = 'image'
            
            photo.save()
            return redirect('gallery')
    else:
        form = PhotoUploadForm()
    return render(request, 'upload_photo.html', {'form': form})

def gallery(request):
    photos = Photo.objects.annotate(
        average_rating=Avg('ratings__score'),
        rating_count=Count('ratings', distinct=True),
        comment_count=Count('comments', distinct=True)
    ).order_by('-id')
    return render(request, 'gallery.html', {'photos': photos})

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    comments = photo.comments.all().order_by('-created_at')
    
    # Add avatar color to each comment
    for comment in comments:
        comment.avatar_color = get_user_avatar_color(comment.user.username)

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
        cache.clear() # Invalidate cache
        return JsonResponse({
            'success': True,
            'comment': {
                'user': new_comment.user.username,
                'text': new_comment.text,
                'created_at': new_comment.created_at.strftime('%b. %d, %Y, %-I:%M %p'),
                'avatar_color': get_user_avatar_color(new_comment.user.username) # Add avatar color
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
        cache.clear() # Invalidate cache
        # Recalculate average rating
        rating_info = photo.ratings.aggregate(average_rating=Avg('score'), rating_count=Count('id'))
        return JsonResponse({
            'success': True,
            'average_rating': round(rating_info['average_rating'] or 0, 1),
            'rating_count': rating_info['rating_count'] or 0
        })
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    if request.user != photo.creator:
        messages.error(request, "You are not authorized to delete this photo.")
        return redirect('photo_detail', photo_id=photo.id)
    
    photo.delete()
    messages.success(request, "Photo deleted successfully!")
    return redirect('gallery')