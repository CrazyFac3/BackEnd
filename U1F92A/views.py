from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from .models import *
from django.utils import timezone
import random
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


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
        :param photo_base64: base64 value of image
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

    @csrf_exempt
    @require_http_methods(["GET", "POST"])
    # @staticmethod
    def register_with_json(request):
        """
        on create - last_activated is the current time.
        :param json_string: json holding image
        :return: None
        """
        body_unicode = request.body
        body = json.loads(body_unicode)
        content = body['photo']
        return UserView.register(request, content)

    @staticmethod
    def display_user(request, user_pk):
        my_user = UserView.get_user_json(request, user_pk)
        return HttpResponse(
            "<h2>Details for User number: " + str(user_pk) +
            ". <br> Date created: " +
            str(my_user["time_created"]) +
            '</h2><br><img src="' + my_user['photo'] + '"/>.'
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

        # json_users = []
        # for user in User.objects.all():
        #     json_users.append(UserView.get_user(request, user.pk))

        users = User.objects.all().values('photo', 'time_created', 'pk')
        users = list(users)
        response = JsonResponse(users, safe=False)

        return response

    @staticmethod
    def get_user_json(request, pk_num):
        # user = User.objects.get(pk=pk_num).values('photo', 'time_created')
        # users = User.objects.all().values('photo', 'time_created', 'pk')
        # users = list(users)
        # for user in users:
        #     if user['pk'] == pk_num:
        #         return JsonResponse(user, safe=False)

        user = User.objects.get(pk=pk_num)
        user_json = {
            'photo': user.photo.base64,
            'time_created': user.time_created,
            'pk': user.pk
        }

        return user_json

        # response = JsonResponse(user, safe=False)
        # return response

    @staticmethod
    def get_random_user(request):
        """
        get a random user
        :param request: the Get request
        :param my_user_pk: the user requesting pk
        :return: User
        """
        all_users = User.objects.all()
        my_user = random.choice(all_users)
        return JsonResponse(UserView.get_user_json(request, my_user.pk))


class PhotoView(View):
    """
    photo management
    """

    @staticmethod
    def get_photo(request, img_pk):
        photo = Photo.objects.get(pk=img_pk)
        photo_json = {
            'base64': photo.base64,
            'time_created': photo.time_created,
            'pk': photo.pk
        }

        return photo_json

    @staticmethod
    @csrf_exempt
    def upload_img(request):
        body_unicode = request.body
        body = json.loads(body_unicode)
        content = body['photo']

        img = Photo(
            base64=content,
            time_created=timezone.now()
        )
        img.save()
        return HttpResponse("created!")

    # @staticmethod
    # def upload_img_json(request):
    #     json_obj = json.loads(request.splitlines()[-1])
    #     return PhotoView.upload_img(request, json_obj['photo'])

    @staticmethod
    @csrf_exempt
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
            str(PhotoView.get_photo(request, photo_pk)["time_created"]) + ".</h2>"
        )

    @staticmethod
    def get_all_images(request):
        """
        :return: All users in a json
        :rtype: JsonResponse
        """
        images = Photo.objects.all().values('base64', 'time_created', 'pk')
        images = list(images)
        response = JsonResponse(images, safe=False)

        return response


class MessageView(View):
    """
    messages management
    """

    @staticmethod
    @csrf_exempt
    def create_new_message(request):

        body_unicode = request.body
        body = json.loads(body_unicode)

        msg = Message(
            sender=User.objects.get(pk=int(body['sender_pk'])),
            receiver=User.objects.get(pk=int(body['receiver_pk'])),
            content_photo=Photo.objects.get(pk=int(body['photo_pk'])),
            content_text=body['content_text'],  # emojis...
            send_time=timezone.now()
        )
        msg.save()

        return HttpResponse("Created!")

    # @staticmethod
    # def create_new_message_with_json(request, json_string):
    #     json_obj = json.loads(json_string)
    #
    #     MessageView.create_new_message(request, json_obj['sender_pk'],
    #                                    json_obj[
    #                                        'receiver_pk', json_obj['photo_pk'],
    #                                        json_obj['photo_pk']])

    @staticmethod
    def get_all_messages(request):
        messages = Message.objects.all().values('sender', 'receiver',
                                                'content_photo', 'content_text'
                                                , 'send_time')
        messages = list(messages)
        response = JsonResponse(messages, safe=False)

        return response

    @staticmethod
    def get_message(requset, pk_msg):
        msg = Message.objects.get(pk=pk_msg)

        msg_json = {
            'sender': msg.sender.pk,
            'receiver': msg.receiver.pk,
            'content_photo': msg.content_photo.base64,
            'content_text': msg.content_text,
            'send_time': msg.send_time,
            'pk': msg.pk
        }

        return msg_json

    @staticmethod
    def get_messages(request):
        params = request.GET
        user_id = params['user_id']
        friend_id = params['friend_id']

        msg_list = Message.object.all().values('sender', 'receiver',
                                               'content_photo', 'content_text',
                                               'send_time')

        msgs_list_final = []

        for message in msg_list:
            if (user_id == message.sender.id
                and friend_id == message.receiver.id) \
                    or (user_id == message.receiver.id
                        and friend_id == message.sender.id):
                msgs_list_final.append(message)

        response = JsonResponse(msgs_list_final, safe=False)

        return response
