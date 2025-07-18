from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EcoActionForm, RegisterForm
from .models import EcoAction, Upload, Profile, Reward, Redemption, EcoCategory
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth import login
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

@login_required
def log_eco_action(request):
    if request.method == 'POST':
        form = EcoActionForm(request.POST, request.FILES)
        if form.is_valid():
            eco_action = form.save(commit=False)
            eco_action.user = request.user
            eco_action.status = 'Pending'
            eco_action.save()
            if form.cleaned_data.get('proof'):
                Upload.objects.create(action=eco_action, file=form.cleaned_data['proof'])
            return redirect('ecoaction_success')
    else:
        form = EcoActionForm()
    return render(request, 'log_action.html', {'form': form})

def ecoaction_success(request):
    return render(request, 'ecoaction_success.html')

@login_required
def profile(request):
    profile = request.user.profile
    approved_actions = EcoAction.objects.filter(user=request.user, status='Approved').order_by('-date_logged')
    # User history tracking
    visits = request.session.get('visits', 0) + 1
    request.session['visits'] = visits
    last_visit = request.COOKIES.get('last_visit')
    response = render(request, 'profile.html', {
        'profile': profile,
        'approved_actions': approved_actions,
        'visits': visits,
        'last_visit': last_visit
    })
    import datetime
    response.set_cookie('last_visit', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return response

@login_required
def rewards(request):
    rewards = Reward.objects.all()
    profile = request.user.profile
    if request.method == 'POST':
        reward_id = request.POST.get('reward_id')
        reward = Reward.objects.get(id=reward_id)
        if profile.points >= reward.cost_in_points:
            profile.points -= reward.cost_in_points
            profile.save()
            Redemption.objects.create(user=request.user, reward=reward)
            messages.success(request, f"You have successfully redeemed: {reward.name}")
        else:
            messages.error(request, "Not enough points to redeem this reward.")
        return redirect('rewards')
    redemptions = Redemption.objects.filter(user=request.user).order_by('-redeemed_on')
    return render(request, 'rewards.html', {'rewards': rewards, 'profile': profile, 'redemptions': redemptions})

def home(request):
    categories = EcoCategory.objects.all()
    return render(request, 'home.html', {'categories': categories})

@login_required
def leaderboard(request):
    search_query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    actions = EcoAction.objects.filter(status='Approved')
    if search_query:
        actions = actions.filter(title__icontains=search_query)
    if category_id:
        actions = actions.filter(category_id=category_id)
    actions = actions.order_by('-date_logged')
    categories = EcoCategory.objects.all()
    top_users = Profile.objects.order_by('-points')[:10]
    return render(request, 'leaderboard.html', {
        'actions': actions,
        'categories': categories,
        'top_users': top_users,
        'search_query': search_query,
        'selected_category': category_id
    })

@staff_member_required
def admin_console(request):
    actions = EcoAction.objects.all().select_related('user', 'category')
    show_rejection_comment = any(a.status == 'Rejected' and a.rejection_comment for a in actions)
    error = None
    error_action_id = None
    # Build a dict of original points for each action - store current points as "original" for approved actions
    # For non-approved actions, we need to track what their original approved value was
    original_points_dict = {}
    for action in actions:
        if action.status == 'Approved':
            # For currently approved actions, current points are the "original approved" points
            original_points_dict[action.id] = action.points
        else:
            # For pending/rejected actions, use last_approved_points if available
            original_points_dict[action.id] = action.last_approved_points if action.last_approved_points is not None else action.points

    if request.method == 'POST':
        # Handle delete
        delete_action_id = request.POST.get('delete_action_id')
        if delete_action_id:
            action_to_delete = EcoAction.objects.get(id=int(delete_action_id))
            if action_to_delete.status == 'Approved':
                profile = action_to_delete.user.profile
                profile.points -= action_to_delete.points
                profile.save()
            action_to_delete.delete()
            return redirect('admin_console')
        # Handle status change
        action_id = request.POST.get('action_id')
        if action_id:
            action_id = int(action_id)
            eco_action = EcoAction.objects.get(id=action_id)
            new_points = int(request.POST.get('edit_points') or 0)
            new_status = request.POST.get('new_status')
            # Get original points from hidden field or fallback to current
            original_points = int(request.POST.get('original_points') or 0)
            # Debug: print what we're processing
            print(f"Processing action {action_id}: current_status={eco_action.status}, new_status={new_status}")
            print(f"Points: new_points={new_points}, original_points={original_points}, current_points={eco_action.points}")
            # Validation: only prevent setting higher points when rejecting (no longer have Pending button)
            if new_status == 'Rejected' and new_points > original_points:
                error = f"Cannot set points higher than original ({original_points}) when rejecting. Point has been set to {original_points}."
                error_action_id = action_id
                print(f"Validation failed: {error}")
                # Do NOT update or save the action, just fall through to render with error
            else:
                print(f"Validation passed, updating action")
                # Only update if validation passes
                eco_action.points = new_points
                eco_action.status = new_status
                if new_status == 'Rejected':
                    eco_action.rejection_comment = request.POST.get('rejection_comment', '')
                elif new_status == 'Approved':
                    eco_action.rejection_comment = ''
                    eco_action.last_approved_points = new_points
                eco_action.save()
                return redirect('admin_console')
    
    return render(request, 'admin_console.html', {
        'actions': actions,
        'show_rejection_comment': show_rejection_comment,
        'error': error,
        'error_action_id': error_action_id,
        'original_points_dict': original_points_dict
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def team(request):
    return render(request, 'team.html')
def privacy(request):
    return render(request, 'privacy.html')
def terms(request):
    return render(request, 'terms.html')
