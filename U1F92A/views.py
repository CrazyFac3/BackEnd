from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import *
from django.utils import timezone


def index(request):
    return HttpResponse("Home Page")


class UserView(View):
    """
    user management
    """

    @staticmethod
    def register(request, uphoto):
        """
        on create - last_activated is the current time.
        :param uphoto: url (base64)
        :return: None
        """
        img = Photo(
            base64=uphoto,
            time_created=timezone.now()
        )
        img.save()

        new_user = User(
            photo=img,
            time_created=timezone.now(),
            last_active=timezone.now()
        )
        new_user.save()

        return HttpResponse("User created. PK of user: {0}. PK of photo: {1}".
                            format(str(img.pk), str(new_user.pk)))

    @staticmethod
    def update_last_active(request, pk_num):
        """
        updating the last_active user attribute
        :param pk_num: int (id/pk number)
        :return: None
        """
        user = User.objects.get(pk=pk_num)
        user.last_active = timezone.now()

    @staticmethod
    def get_all_users(request):
        """
        Returning all users list
        :return: list
        """
        return User.objects.all()

    @staticmethod
    def get_user(request, pk_num):
        return User.objects.get(pk=pk_num)


class PhotoView(View):
    """
    photo management
    """

    @staticmethod
    def get_photo(request, img_pk):
        return Photo.objects.get(pk=img_pk)

    @staticmethod
    def upload_img(request, photo_url):
        img = Photo(
            url=photo_url,
            time_created=timezone.now()
        )
        img.save()
        return HttpResponse("created!")

    @staticmethod
    def display_all_photos(request):
        all_photos = Photo.objects.all()
        html = ''
        for photo in all_photos:
            url = str(photo.pk) + '/'
            html += '<a href="' + url + '"><img src="' + photo.base64 + \
                    '"></img></a><br>'
        return HttpResponse(html)

    @staticmethod
    def details_photo(request, photo_pk):
        return HttpResponse(
            "<h2>Details for Photo number: " + str(photo_pk) +
            ". <br> Date created: " +
            str(PhotoView.get_photo(request, photo_pk).time_created)+ ".</h2>"
        )


class MessageView(View):
    """
    messages management
    """

    @staticmethod
    def create_new_message(request, sender_pk, reciever_pk, photo_pk, text_str):
        msg = Message(
            sender=UserView.get_user(request, sender_pk),
            reciever=UserView.get_user(request, reciever_pk),
            content_photo=PhotoView.get_photo(request, photo_pk),
            content_text=text_str, # emojis...
            send_time=timezone.now()
        )
        msg.save()

    @staticmethod
    def get_all_messages(request):
        return Message.objects.all()

    @staticmethod
    def get_message(requset, pk_msg):
        return Message.objects.get(pk=pk_msg)
