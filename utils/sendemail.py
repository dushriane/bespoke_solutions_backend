from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_email(full_name, code, subject, rec, template_name="emails/resetpasswordotp_email.html"):
    context = {
        "name": full_name,
        "reset_password_code": code,
        "message": subject,
    }
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [rec],
    )
    email.attach_alternative(html_content, "text/html")
    return email.send()
