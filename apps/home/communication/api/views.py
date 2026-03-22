from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view

from communication.models import Subscriber
from .serializers import ContactSerializer, SubscriberSerializer

from communication.send_emails import EmailTemplates, EmailSender

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

class SubscriberViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    # Define separate methods for each action
    def subscribe(self, request):
        return self.manage_subscription(request)

    def unsubscribe(self, request, email):
        return self.manage_subscription(request)

    def resubscribe(self, request, email):
        return self.manage_subscription(request)

    def manage_subscription(self, request):
        email = request.data.get('email')
        action_type = request.data.get('action_type')  # 'unsubscribe', 'resubscribe', 'subscribe'

        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        subscriber = Subscriber.objects.filter(email=email).first()

        if action_type == 'unsubscribe':
            if subscriber:
                subscriber.is_subscribed = False
                subscriber.save()
                return Response({'message': 'You have been unsubscribed successfully.'})
            else:
                return Response({'message': 'Email not found.'}, status=status.HTTP_400_BAD_REQUEST)
        
        elif action_type == 'resubscribe':
            if subscriber:
                subscriber.is_subscribed = True
                subscriber.save()
                return Response({'message': 'You have been resubscribed successfully.'})
            else:
                return Response({'message': 'Email not found.'}, status=status.HTTP_400_BAD_REQUEST)
        
        elif action_type == 'subscribe':
            if subscriber:
                subscriber.is_subscribed = True
                subscriber.save()
                serializer = SubscriberSerializer(subscriber)
            else:
                data = {'email': email, 'is_subscribed': True}
                serializer = SubscriberSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response({'error': 'Invalid data.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid action_type.'}, status=status.HTTP_400_BAD_REQUEST)


# class SubscriberViewSet(
#     mixins.CreateModelMixin, mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin, viewsets.GenericViewSet
# ):
#     queryset = Subscriber.objects.all()
#     serializer_class = SubscriberSerializer

#     @action(detail=False, methods=['POST'])
#     def manage_subscription(self, request):
#         email = request.data.get('email')
#         action_type = request.data.get('action_type')  # 'unsubscribe', 'resubscribe', 'subscribe'

#         if not email:
#             return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

#         subscriber = Subscriber.objects.filter(email=email).first()

#         if action_type == 'unsubscribe':
#             if subscriber:
#                 subscriber.is_subscribed = False
#                 subscriber.save()
#                 return Response({'message': 'You have been unsubscribed successfully.'})
#             else:
#                 return Response({'message': 'Email not found.'}, status=status.HTTP_400_BAD_REQUEST)
        
#         elif action_type == 'resubscribe':
#             if subscriber:
#                 subscriber.is_subscribed = True
#                 subscriber.save()
#                 return Response({'message': 'You have been resubscribed successfully.'})
#             else:
#                 return Response({'message': 'Email not found.'}, status=status.HTTP_400_BAD_REQUEST)
        
#         elif action_type == 'subscribe':
#             if subscriber:
#                 subscriber.is_subscribed = True
#                 subscriber.save()
#                 serializer = SubscriberSerializer(subscriber)
#             else:
#                 data = {'email': email, 'is_subscribed': True}
#                 serializer = SubscriberSerializer(data=data)
#                 if serializer.is_valid():
#                     serializer.save()
#                 else:
#                     return Response({'error': 'Invalid data.'}, status=status.HTTP_400_BAD_REQUEST)
#             return Response(serializer.data)
#         else:
#             return Response({'error': 'Invalid action_type.'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def submit_contact(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            serializer = ContactSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                # You can add code here to send an email notification if needed
                email_body_html = EmailTemplates.email_confirmation(serializer.data['name'])
                email_data = {
                    'email': serializer.data['email'],
                    'body': email_body_html,
                    'subject': serializer.data['subject']
                }
                EmailSender.send_email(email_data)

                return JsonResponse({'message': 'Your request has been submitted successfully'})
            else:
                return JsonResponse({'errors': serializer.errors}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



# class SubscriberViewSet(
#     mixins.CreateModelMixin, mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin, viewsets.GenericViewSet
#     ):
#     queryset = Subscriber.objects.all()
#     serializer_class = SubscriberSerializer
    
#     def unsubscribe(self, request, *args, **kwargs):
#         email = kwargs.get('email')
#         subscriber = Subscriber.objects.filter(email=email).first()
#         if subscriber:
#             subscriber.is_subscribed = False
#             subscriber.save()
#             return Response({'message': 'You have been unsubscribed successfully.'})
#         else:
#             return Response({'message': 'Email not found.'}, status=400)

#     def resubscribe(self, request, *args, **kwargs):
#         email = kwargs.get('email')
#         subscriber = Subscriber.objects.filter(email=email).first()
#         if subscriber:
#             subscriber.is_subscribed = True
#             subscriber.save()
#             return Response({'message': 'You have been resubscribed successfully.'})
#         else:
#             return Response({'message': 'Email not found.'}, status=400)
        

# @api_view(['POST'])
# def subscribe(request):
#     email = request.data.get('email')
#     if email:
#         subscriber = Subscriber.objects.filter(email=email).first()
#         if subscriber:
#             # If the subscriber already exists, update is_subscribed to True
#             subscriber.is_subscribed = True
#             subscriber.save()
#             serializer = SubscriberSerializer(subscriber)
#         else:
#             # If the subscriber doesn't exist, create a new Subscriber object
#             data = {'email': email, 'is_subscribed': True}
#             serializer = SubscriberSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#         return Response(serializer.data)
#     else:
#         return Response({'error': 'Email is required.'})
    


# from django.shortcuts import render, redirect
# from .forms import ContactForm
# from .send_emails import EmailTemplates, EmailSender

# def contact_view(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
      
#         if form.is_valid():
#             form.save()
#             # You can add code here to send an email notification if needed

#             email_body_html = EmailTemplates.email_confirmation(form.cleaned_data['name'])
            
#             email = form.cleaned_data['email']
#             email_subject = form.cleaned_data['subject']
#             # email_body_html = form.cleaned_data['message']

#             data = {'email': email, 'body': email_body_html, 'subject': email_subject}
            
#             EmailSender.send_email(data)

#             return redirect('contact_success')  # Redirect to a success page
        
#         else:
#             print('Form is not valid:', form.errors)

#     else:
#         form = ContactForm()
#         print('GET request received')

    
#     return render(request, 'contact.html', {'form': form})

# def contact_success(request):
#     return render(request, 'contact_success.html')


# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# import json

# @csrf_exempt
# @api_view(['POST'])
# def submit_contact(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             serializer = ContactSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 # You can add code here to send an email notification if needed
#                 email_body_html = EmailTemplates.email_confirmation(serializer.data['name'])
#                 email_data = {
#                     'email': serializer.data['email'],
#                     'body': email_body_html,
#                     'subject': serializer.data['subject']
#                 }
#                 EmailSender.send_email(email_data)

#                 return JsonResponse({'message': 'Your request has been submitted successfully'})
#             else:
#                 return JsonResponse({'errors': serializer.errors}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)