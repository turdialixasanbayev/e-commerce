from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == "POST":
        data = request.POST

        phone_number = data.get('phone_number')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        remember_me = data.get('remember_me')

        if len(password) < 8:
            messages.error(request, "🔒 Password must be at least 8 characters long!")
            return redirect('register')

        if not all([phone_number, password, confirm_password, remember_me]):
            messages.error(request, "❌ Please fill in all fields!")
            return redirect('register')
        
        pattern = r'^\+?\d{9,15}$'
        if not re.match(pattern, phone_number):
            messages.error(request, "📱 Invalid phone number format! Example: +998901234567")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "❌ Passwords do not match!")
            return redirect('register')

        if CustomUser.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "📱 This phone number is already registered!")
            return redirect('register')

        user = CustomUser.objects.create_user(phone_number=phone_number, password=password)
        user.save()
        login(request, user)

        if remember_me == "on":
            request.session.set_expiry(1209600) # 14 days
        else:
            request.session.set_expiry(0)

        messages.success(request, "🎉 Account created successfully! You are now logged in 🙌")
        return redirect('profile')

    return render(request, 'register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == "POST":
        data = request.POST

        phone_number = data.get('phone_number')
        password = data.get('password')
        remember_me = data.get('remember_me')

        user = authenticate(request, phone_number=phone_number, password=password)

        if user is not None:
            login(request, user)

            if remember_me == "on":
                request.session.set_expiry(1209600) # 14 days
            else:
                request.session.set_expiry(0)

            messages.success(request, 'You are logged in successfully ✅')
            return redirect('profile')
        else:
            messages.error(request, 'Incorrect phone number or password ❌')
            return redirect('login')

    return render(request, "login.html")

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You are logged out successfully ✅')
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def delete_account(request):
    user = request.user
    user.delete()
    messages.success(request, "🗑️ Account successfully deleted 👋")
    return redirect('home')

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not current_password or not new_password or not confirm_password:
            messages.error(request, "⚠️ Please fill in all fields!")
            return redirect('change_password')

        if not request.user.check_password(current_password):
            messages.error(request, "❌ Current password is incorrect!")
            return redirect('change_password')

        if len(new_password) < 8:
            messages.error(request, "🔒 Password must be at least 8 characters long!")
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, "❌ Passwords do not match!")
            return redirect('change_password')

        if current_password == new_password:
            messages.error(request, "⚠️ New password cannot be the same as current password!")
            return redirect('change_password')

        user = request.user
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "✅ Password successfully changed and you're still logged in!")
        return redirect('profile')

    return render(request, 'change_password.html')
