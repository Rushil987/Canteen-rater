from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish, Rating
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Count

def menu_list(request):
    dishes = Dish.objects.all()
    return render(request, 'menu/menu_list.html', {'dishes': dishes})

def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, pk=dish_id)
    if request.method == 'POST':
        rating_value = int(request.POST['rating'])
        review_text = request.POST.get('review', '')
        Rating.objects.create(dish=dish, user=request.user, rating=rating_value, review=review_text)
        return redirect('dish_detail', dish_id=dish.id)
    ratings = dish.ratings.all()
    avg_rating = dish.average_rating()
    return render(request, 'menu/dish_detail.html', {
        'dish': dish,
        'ratings': ratings,
        'avg_rating': avg_rating,
    })

def leaderboard_view(request):
    dishes = Dish.objects.annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')[:10]
    return render(request, 'menu/leaderboard.html', {'dishes': dishes})

@login_required
def admin_dashboard(request):
    today = timezone.now().date()
    last_week = today - timedelta(days=7)

    avg_ratings_per_day = Rating.objects.filter(created_at__date__range=(last_week, today)) \
        .values('created_at__date') \
        .annotate(avg=Avg('rating')) \
        .order_by('created_at__date')

    ratings_per_day = Rating.objects.filter(created_at__date__range=(last_week, today)) \
        .values('created_at__date') \
        .annotate(count=Count('id')) \
        .order_by('created_at__date')

    most_liked = Dish.objects.annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating').first()
    least_liked = Dish.objects.annotate(avg_rating=Avg('ratings__rating')) \
                              .exclude(ratings__isnull=True) \
                              .order_by('avg_rating').first()

    return render(request, 'menu/admin_dashboard.html', {
        'avg_ratings_per_day': avg_ratings_per_day,
        'ratings_per_day': ratings_per_day,
        'most_liked': most_liked,
        'least_liked': least_liked,
    })
