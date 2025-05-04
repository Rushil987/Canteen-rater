from django.db import models
from django.contrib.auth.models import User

class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def average_rating(self):
        avg = self.ratings.aggregate(avg=models.Avg('rating'))['avg']
        return round(avg, 2) if avg else None

    def __str__(self):
        return self.name

class Rating(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.dish.name} ({self.rating})"
