from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
import re
from django.contrib.auth.decorators import login_required


def register_view(request):
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
        return redirect('home')

    return render(request, 'register.html')

def login_view(request):
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
            return redirect('home')
        else:
            messages.error(request, 'Incorrect phone number or password ❌')
            return redirect('login')

    return render(request, "login.html")

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You are logged out successfully ✅')
    return redirect('home')
