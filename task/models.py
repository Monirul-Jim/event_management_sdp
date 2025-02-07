from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.name


# class Participant(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     events = models.ManyToManyField(Event, related_name='participants')

#     def __str__(self):
#         return self.name
class Participant(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='participant_profile', null=True, blank=True)
    events = models.ManyToManyField(Event, related_name='participants')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=Participant)
def notify_user_participate(sender, instance, created, **kwargs):
    if created and instance.user:  # Check if it's a new participant
        event_names = ", ".join(
            [event.name for event in instance.events.all()])

        subject = "Thank You for Joining Our Event!"
        message = f"Hello {instance.user.username},\n\n" \
            f"Thank you for joining our event.\n" \
            f"Your joined event(s): {event_names}.\n\n" \
            "We look forward to seeing you there!\n\n" \
            "Best regards,\nEvent Team"

        send_mail(
            subject,
            message,
            "lrbmonirulislamjim@gmail.com",
            [instance.user.email],
            fail_silently=False,
        )
