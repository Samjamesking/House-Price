from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, UserProfileUpdateForm
from prediction.models import PredictionHistory
from django.db.models import Avg

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}! You can now log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.profile)

    # Calculate user prediction statistics
    user_predictions = PredictionHistory.objects.filter(user=request.user)
    total_predictions = user_predictions.count()
    avg_price = user_predictions.aggregate(Avg('predicted_price_usd'))['predicted_price_usd__avg'] or 0.0

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'total_predictions': total_predictions,
        'avg_price': avg_price,
    }
    return render(request, 'accounts/profile.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('landing')
