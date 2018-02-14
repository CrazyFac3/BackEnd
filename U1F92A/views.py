from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
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
    def register(request, photo_base64):
        """
        on create - last_activated is the current time.
        :param uphoto: url (base64)
        :return: None
        """
        img = Photo(
            base64=photo_base64,
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
                            format(str(new_user.pk), str(img.pk)))

    @staticmethod
    def display_user(request, user_pk):
        return HttpResponse(
            "<h2>Details for User number: " + str(user_pk) +
            ". <br> Date created: " +
            str(UserView.get_user(request, user_pk).time_created) +
            '</h2><br><img src="' + UserView.get_user(request, user_pk).photo.
            base64 + '"/>.'
        )

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
        :return: All users in a json
        :rtype: JsonResponse
        """
        users = User.objects.all().values('photo', 'time_created',
                                          'last_active')
        users = list(users)
        response = JsonResponse(users, safe=False)

        return response

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
            str(PhotoView.get_photo(request, photo_pk).time_created) + ".</h2>"
        )

    @staticmethod
    def get_all_images(request):
        """
        :return: All users in a json
        :rtype: JsonResponse
        """
        images = Photo.objects.all().values('photo', 'time_created',
                                            'last_active')
        images = list(images)
        response = JsonResponse(images, safe=False)

        return response


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
            content_text=text_str,  # emojis...
            send_time=timezone.now()
        )
        msg.save()

    @staticmethod
    def get_all_messages(request):
        return Message.objects.all()

    @staticmethod
    def get_message(requset, pk_msg):
        return Message.objects.get(pk=pk_msg)
