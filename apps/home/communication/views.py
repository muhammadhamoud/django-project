from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Subscriber

from django.shortcuts import render, redirect
from .forms import ContactForm
from .send_emails import EmailTemplates, EmailSender

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
      
        if form.is_valid():
            form.save()
            # You can add code here to send an email notification if needed

            email_body_html = EmailTemplates.email_confirmation(form.cleaned_data['name'])
            
            email = form.cleaned_data['email']
            email_subject = form.cleaned_data['subject']
            # email_body_html = form.cleaned_data['message']

            data = {'email': email, 'body': email_body_html, 'subject': email_subject}
            
            EmailSender.send_email(data)

            return redirect('contact_success')  # Redirect to a success page
        
        else:
            print('Form is not valid:', form.errors)

    else:
        form = ContactForm()
        print('GET request received')

    
    return render(request, 'contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact_success.html')




