from events.models import Event
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = (
            f"{settings.FRONTEND_URL}/events/activate/{instance.id}/{token}/"
        )

        subject = "Activate Your Account"
        message = (
            f"Hi {instance.username},\n\n"
            f"Please activate your account by clicking the link below:\n"
            f"{activation_url}\n\n"
            "Thank you for joining EventManager!"
        )

        recipient_list = [instance.email]

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")


@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_confirmation_email(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)
            subject = f"RSVP Confirmed for {instance.name}"
            message = (
                f"Hi {user.username},\n\n"
                f'You have successfully RSVP’d to "{instance.name}" scheduled on {instance.date} at {instance.time}.\n\n'
                "Thank you for your interest!"
            )

            recipient_list = [user.email]

            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            except Exception as e:
                print(f"Failed to send email to {user.email}: {str(e)}")


@receiver(post_save, sender=User)
def assign_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name="Participant")
        instance.groups.add(group)
