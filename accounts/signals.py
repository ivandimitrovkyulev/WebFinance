from django.dispatch import receiver
from django.core.mail import send_mail
from allauth.account.signals import email_confirmed

from webfinance.settings import DEFAULT_FROM_EMAIL

from .models import UserAccount


# Mark this function as a receiver of 'email_confirmed' signal
@receiver(email_confirmed)
def send_email_notification_handler(sender, **kwargs) -> bool:
    user = kwargs['request'].user

    all_admins = [user.email for user in UserAccount.objects.all().filter(is_superuser=True)]

    subject = "New Sign-Up to WebFinance"
    message = f"This is an automated message from WebFinance.\n\n"\
              f"A user has just verified their email address:\n"\
              f"User:  {user.username}\n"\
              f"Email: {user.email}\n\n"
    send_mail(
        subject=subject,
        message=message,
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=all_admins,
    )
    return True
