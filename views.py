from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from .models import Consumption, DailyGoal
from .forms import ConsumptionForm

@login_required
def dashboard(request):
    today = timezone.localdate()
    entries = Consumption.objects.filter(user=request.user, eaten_at__date=today)

    total_today = entries.annotate(
        total_calories=ExpressionWrapper(
            F('food__calories_per_100g') * F('quantity_g') / 100,
            output_field=FloatField()
        )
    ).aggregate(total=Sum('total_calories'))['total'] or 0

    # Get the user's latest daily goal
    daily_goal = DailyGoal.objects.filter(user=request.user).first()
    remaining = daily_goal.calories_goal - total_today if daily_goal else None

    context = {
        "entries": entries,
        "total_today": round(total_today, 2),
        "goal": daily_goal.calories_goal if daily_goal else "Not Set",
        "remaining": round(remaining, 2) if remaining is not None else "N/A",
    }

    return render(request, "calories/dashboard.html", context)


@login_required
def add_entry(request):
    if request.method == "POST":
        form = ConsumptionForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect("calories:dashboard")
    else:
        form = ConsumptionForm()
    return render(request, "calories/add_entry.html", {"form": form})


