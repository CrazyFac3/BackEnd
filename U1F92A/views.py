from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import *
from django.utils import timezone


def index(request):
    return HttpResponse("Hello, world. You're at polls index.")


class UserView(View):
    """
    user management
    """

    @staticmethod
    def register(uphoto):
        """
        on create - last_activated is the current time.
        :param uphoto: Photo (U1F92A.models)
        :return: None
        """
        # upload_img(uphoto)
        new_user = User(
            photo=uphoto,
            time_created=timezone.now(),
            last_active=timezone.now()
        )
        new_user.save()

    @staticmethod
    def update_last_active(pk_num):
        """
        updating the last_active user attribute
        :param pk_num: int (id/pk number)
        :return: None
        """
        user = User.objects.get(pk=pk_num)
        user.last_active = timezone.now()

    @staticmethod
    def get_all_users():
        """
        Returning all users list
        :return: list
        """
        return User.objects.all()

    @staticmethod
    def get_user(pk_num):
        return User.objects.get(pk=pk_num)


class PhotoView(View):
    """
    photo management
    """

    @staticmethod
    def get_photo(img_pk):
        return Photo.objects.get(pk=img_pk)

    # @staticmethod
    # def upload_img(url):
    # Rotem will take care


class MessageView(View):
    """
    messages management
    """

    @staticmethod
    def create_new_message(sender_pk, reciever_pk, photo_pk, text_str):
        msg = Message(
            sender=UserView.get_user(sender_pk),
            reciever=UserView.get_user(reciever_pk),
            content_photo=PhotoView.get_photo(photo_pk),
            content_text=text_str, # emoji...
            send_time=timezone.now()
        )

    @staticmethod
    def get_all_messages():
        return Message.objects.all()
    
    @staticmethod
    def get_message(pk_msg):
        return Message.objects.get(pk=pk_msg)





