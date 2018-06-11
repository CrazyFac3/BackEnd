from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete


class Photo(models.Model):
    """
    TODO: Change ASAP, the image should NOT be saved as base64
    """
    base64 = models.CharField(max_length=10000)
    time_created = models.DateTimeField('Date created')

    def __str__(self):
        return str(self.pk)


class User(models.Model):
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE)
    time_created = models.DateTimeField('date created')
    last_active = models.DateTimeField('last active date')

    def __str__(self):
        return str(self.pk)

    def delete(self):
        self.photo.delete()
        return super(User, self).delete()


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='maps')
    content_photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    content_text = models.CharField(max_length=1000)  # Emoji
    send_time = models.DateTimeField('date sent')

    def __str__(self):
        if not self.content_text:
            return "Photo Message " + str(self.pk)
        else:
            return "Text Message " + str(self.pk)


@receiver(pre_delete, sender=User)
def delete_user_image(sender, instance, **kwargs):
    """
    Releases the resources that the users used. his Image is deleted and
    all of his messages.

    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    for message in instance.message_set.all():
        message.delete()
