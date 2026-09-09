"""Guest Reviews, Ratings Analytics, and Management Replies Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.reviews.models import Review
from apps.accounts.decorators import module_permission_required

@login_required
def review_list_view(request):
    """List of all customer ratings and dining reviews."""
    branch = request.user.branch
    reviews = Review.objects.all().select_related('customer', 'branch', 'order')
    
    if branch:
        reviews = reviews.filter(branch=branch)
        
    rating_filter = request.GET.get('rating')
    if rating_filter:
        reviews = reviews.filter(overall_rating=rating_filter)

    reviews = reviews.order_by('-created_at')

    avg_rating = 0
    if reviews.exists():
        avg_rating = round(sum(r.overall_rating for r in reviews) / reviews.count(), 1)

    return render(request, 'reviews/review_list.html', {
        'reviews': reviews,
        'avg_rating': avg_rating,
        'rating_filter': rating_filter,
    })

@login_required
def review_reply_view(request, review_id):
    """Restaurant manager replies to customer review."""
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        response_text = request.POST.get('response', '').strip()
        if response_text:
            review.management_response = response_text
            review.responded_by = request.user
            review.responded_at = timezone.now()
            review.save(update_fields=['management_response', 'responded_by', 'responded_at'])
            messages.success(request, "Management response published.")
    return redirect('reviews:list')
