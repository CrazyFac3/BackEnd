from django.db import models
from django.utils import timezone


class Photo(models.Model):
    url = models.CharField(max_length=10000)
    time_created = models.DateTimeField('Date created')

    def __str__(self):
        return str(self.pk)


class User(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    time_created = models.DateTimeField('date created')
    last_active = models.DateTimeField('last active date')

    def __str__(self):
        return str(self.pk)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='maps')
    content_photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    content_text = models.CharField(max_length=1000)
    send_time = models.DateTimeField('date sent')

    def __str__(self):
        if not self.content_text:
            return "Photo Message " + str(self.pk)
        else:
            return "Text Message " + str(self.pk)






