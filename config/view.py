from django.shortcuts import render

from django.contrib.auth.decorators import login_required


# @login_required # Uncomment this line to require login for the home view
def home_view(request):
    return render(request, 'index.html')
