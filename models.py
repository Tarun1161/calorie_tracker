from django.db import models
from django.contrib.auth.models import User

class FoodItem(models.Model):
    name = models.CharField(max_length=200)
    calories_per_100g = models.PositiveIntegerField()
    protein_g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    carbs_g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    fats_g = models.DecimalField(max_digits=6, decimal_places=2, null=True , blank=True)

    def __str__(self):
        return self.name
    
class Consumption(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    food=models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    quantity_g=models.FloatField()
    eaten_at=models.DateTimeField(auto_now_add=True)


    @property
    def total_calories(self):
        return(self.food.calories_per_100g *self.quantity_g)/100
    def __str__(self):
        return f"{self.user.username} - {self.food.name} - {self.quantity_g}g"

class DailyGoal(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    calories_goal=models.PositiveIntegerField(default=2000)

    def __str__(self):
        return f"{self.user.username} - {self.calories_goal} kcal"
    