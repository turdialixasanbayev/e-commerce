from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import ContactMessage


class ContactView(View):
    template_name = 'contact.html'

    def get(self, request):
        context = {'text': "Welcome to Contact View!"}
        return render(request=request, template_name=self.template_name, context=context)
    
    def post(self, request):
        url = request.META.get("HTTP_REFERER")
        data = request.POST
        name = data.get("name")
        email = data.get('email')
        message = data.get('message')

        if name and email and message:
            contact = ContactMessage.objects.create(name=name, email=email, message=message)
            contact.save()
            messages.success(request, "Message sent!")
            return redirect(url)
        else:
            messages.error(request, "All require!")
            return redirect(url)
