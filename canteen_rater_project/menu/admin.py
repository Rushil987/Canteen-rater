from django.contrib import admin
from .models import Dish, Rating

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0

class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [RatingInline]

class RatingAdmin(admin.ModelAdmin):
    list_display = ('dish', 'user', 'rating', 'created_at')
    list_filter = ('dish', 'rating')

admin.site.register(Dish, DishAdmin)
admin.site.register(Rating, RatingAdmin)
