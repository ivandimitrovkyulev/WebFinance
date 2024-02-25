from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # Signal receivers are connected in the ready() method
    def ready(self):
        from .signals import email_confirmed, send_email_notification_handler
        # Explicitly connect a signal handler.
        email_confirmed.connect(send_email_notification_handler)
