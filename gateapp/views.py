from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .models import Visitor, Guard
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta
from django.shortcuts import get_object_or_404

def custom_logout(request):
    logout(request)
    return redirect('login')
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif hasattr(user, 'guard'):
                return redirect('guard_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def guard_dashboard(request):
    if not hasattr(request.user, 'guard'):
        return redirect('login')
    
    if request.method == 'POST':
        name = request.POST.get('name', '')
        purpose = request.POST.get('purpose', '')
        mobile_number = request.POST.get('mobile_number', '')

        Visitor.objects.create(
            name=name,
            purpose=purpose,
            mobile_number=mobile_number,
            recorded_by=request.user.guard,
            entry_time=now(),
            exit_time=now() + timedelta(minutes=30)  # Auto-set exit time
        )
        return redirect('guard_dashboard')
    
    visitors = Visitor.objects.filter(recorded_by=request.user.guard).order_by('-entry_time')
    return render(request, 'guard_dashboard.html', {'visitors': visitors})

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('login')
    
    guards = Guard.objects.all()
    visitors = Visitor.objects.all().order_by('-entry_time')  # Show latest visitors first
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        
        # Create a new User and link to Guard model
        user = User.objects.create_user(username=username, password=password)
        Guard.objects.create(user=user, name=name, phone=phone)

        
        return redirect('admin_dashboard')
    
    return render(request, 'admin_dashboard.html', {'guards': guards, 'visitors': visitors})
