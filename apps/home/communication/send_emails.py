from django.core.mail import EmailMessage
from django.conf import settings

website_name = settings.WEBISTE_NAME
email_style = """
    <style>
    /* CSS styling */
    body {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 16px;
        line-height: 1.5;
        color: #333333;
        background-color: #a2a1a1;
        padding: 20px;
    }
    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        margin-top: 0;
    }
    a {
        color: #0e273a;
    }
    .button {
        display: inline-block;
        font-weight: 400;
        color: #ffffff;
        text-align: center;
        vertical-align: middle;
        background-color: #0e273a;
        border: 1px solid #0e273a;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        text-decoration: none;
    }
    .button:hover {
        background-color: #3e607e;
        border-color: #3e607e;
    }
    </style>
"""

class EmailSender:
    @staticmethod
    def send_email(data):
        email = EmailMessage(to=[data['email']], subject=data['subject'], body=data['body'])
        
        # Optional: add a plain text version of the email
        email.content_subtype = 'html'
        email.send(fail_silently=True)


class EmailTemplates:
    def email_verfication_template(full_name, url):
        email_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8" />
                <title>Example Email Template</title>
                {email_style}
            </head>
            <body>
                <h1>Email Verification Confirmation</h1>
                <p>Dear {full_name},</p>
                <p>
                Thank you for signing up for our {website_name} service. To complete your registration,
                please click on the link below to verify your email address:
                </p>
                <p style="text-align: left"><a href="{url}" class="button">Verify Email Address</a></p>
            
                <p>If you did not sign up for our service, please disregard this email.</p>
                <p>Best regards,</p>
                <p>The {website_name} Team</p>
                <hr />
            </body>
            </html>
        """
        return email_body
    
    def email_confirmation(full_name):

        email_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8" />
                <title>Contact Request Confirmation</title>
                {email_style}
            </head>
            <body>
                <h1>Thank you for contacting {website_name}</h1>
                <p>Dear {full_name},</p>
                <p>
                Thank you for contacting us. We have received your request, and our team will get back to you shortly.
                </p>
                <p>
                In the meantime, if you have any urgent questions or concerns, please feel free to reply to this email.
                </p>

                <p>If you did not initiate this contact request, please disregard this email.</p>
                <p>Best regards,</p>
                <p>The {website_name} Team</p>
                <hr />
            </body>
            </html>
        """
        return email_body
    

