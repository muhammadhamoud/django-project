from django.shortcuts import render
from django_ratelimit.decorators import ratelimit

from .forms import ContactForm
from .send_emails import EmailTemplates, EmailSender


# def get_client_ip(request):
#     x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
#     if x_forwarded_for:
#         return x_forwarded_for.split(",")[0].strip()
#     return request.META.get("REMOTE_ADDR")


def get_client_ip(request):
    # Cloudflare
    cf_ip = request.META.get("HTTP_CF_CONNECTING_IP")
    if cf_ip:
        return cf_ip

    # Proxy setups
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    x_real_ip = request.META.get("HTTP_X_REAL_IP")
    if x_real_ip:
        return x_real_ip

    # Default fallback
    return request.META.get("REMOTE_ADDR")


def get_user_agent(request):
    return request.META.get("HTTP_USER_AGENT", "")


@ratelimit(key="ip", rate="5/10m", method="POST", block=False)
def contact_view(request):
    success = False
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)

        if getattr(request, "limited", False):
            form.add_error(None, "Too many submissions. Please wait a few minutes and try again.")
        elif form.is_valid():
            contact = form.save(commit=False)
            contact.ip_address = get_client_ip(request)
            contact.user_agent = get_user_agent(request)
            contact.save()

            email_body_html = EmailTemplates.email_confirmation(contact.name)
            data = {
                "email": contact.email,
                "body": email_body_html,
                "subject": contact.subject,
            }
            EmailSender.send_email(data)

            success = True
            form = ContactForm()

    return render(
        request,
        "communication/contact.html",
        {
            "form": form,
            "success": success,
        },
    )



from .forms import SubscriberForm
from .models import Subscriber


@ratelimit(key="ip", rate="5/10m", method="POST", block=False)
def subscriber_view(request):
    success = False
    success_title = ""
    success_message = ""
    form = SubscriberForm()

    if request.method == "POST":
        form = SubscriberForm(request.POST)

        if getattr(request, "limited", False):
            form.add_error(None, "Too many requests. Please wait a few minutes and try again.")
        elif form.is_valid():
            email = form.cleaned_data["email"]
            action = form.cleaned_data["action"]

            subscriber = Subscriber.objects.filter(email=email).first()

            if action == SubscriberForm.ACTION_SUBSCRIBE:
                if subscriber:
                    if subscriber.is_subscribed:
                        success_title = "Already subscribed"
                        success_message = "This email address is already subscribed to our updates."
                    else:
                        subscriber.is_subscribed = True
                        subscriber.save(update_fields=["is_subscribed", "updated_at"])
                        success_title = "Subscription restored"
                        success_message = "Your email has been successfully resubscribed."
                else:
                    Subscriber.objects.create(email=email, is_subscribed=True)
                    success_title = "Subscription successful"
                    success_message = "Thank you for subscribing to our updates."

                success = True
                form = SubscriberForm(initial={"action": SubscriberForm.ACTION_SUBSCRIBE})

            elif action == SubscriberForm.ACTION_UNSUBSCRIBE:
                if subscriber:
                    if subscriber.is_subscribed:
                        subscriber.is_subscribed = False
                        subscriber.save(update_fields=["is_subscribed", "updated_at"])
                        success_title = "Unsubscribed successfully"
                        success_message = "You have been removed from our mailing list."
                    else:
                        success_title = "Already unsubscribed"
                        success_message = "This email address is already unsubscribed."
                else:
                    success_title = "Email not found"
                    success_message = "We could not find this email in our subscriber list."

                success = True
                form = SubscriberForm(initial={"action": SubscriberForm.ACTION_SUBSCRIBE})

            elif action == SubscriberForm.ACTION_RESUBSCRIBE:
                if subscriber:
                    if subscriber.is_subscribed:
                        success_title = "Already subscribed"
                        success_message = "This email address is already subscribed."
                    else:
                        subscriber.is_subscribed = True
                        subscriber.save(update_fields=["is_subscribed", "updated_at"])
                        success_title = "Resubscribed successfully"
                        success_message = "Welcome back. Your subscription has been reactivated."
                else:
                    Subscriber.objects.create(email=email, is_subscribed=True)
                    success_title = "Subscription created"
                    success_message = "This email was not previously registered, so a new active subscription was created."

                success = True
                form = SubscriberForm(initial={"action": SubscriberForm.ACTION_SUBSCRIBE})

    return render(
        request,
        "communication/subscriber.html",
        {
            "form": form,
            "success": success,
            "success_title": success_title,
            "success_message": success_message,
        },
    )