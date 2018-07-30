import json
import random

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import *


# todo: check get_friends function


def index(request):
    def filter_api_function(cls, func):
        return (callable(getattr(cls, func)) and
                not func.startswith('_') and
                func not in dir(View))

    methods = {
        cls.__name__[:-4]: [f for f in dir(cls) if filter_api_function(cls, f)]
        for cls in (UserView, MessageView, PhotoView)
    }

    return render(request, "api_list.html", {'methods': methods})


class UserView(View):
    """
    user management
    """

    @staticmethod
    def get_all_users_json(_):
        """
        :return: All users in a json
        :rtype: JsonResponse
        """
        users = User.objects.all().values('photo', 'time_created', 'pk')
        users = list(users)

        return JsonResponse(users, safe=False)

    @staticmethod
    def get_user_html(request, user_pk):
        """
        :param request: the request
        :type request: django.core.handlers.wsgi.WSGIRequest
        :param user_pk: user id
        :type user_pk: int
        :return: detail for the specific user
        :rtype: HttpResponse
        """
        user = User.objects.get(pk=user_pk)

        return render(request, 'detail.html', {
            'entity': 'User',
            'number': user_pk,
            'time_created': user.time_created,
            'photo_base64': user.photo.base64
        })

    @staticmethod
    def get_user_json(_, user_pk):
        """
        :param user_pk: user id
        :type user_pk: int
        :return: get specific user in a json
        :rtype: JsonResponse
        """
        user = User.objects.get(pk=user_pk)
        return JsonResponse({
            'pk': user.pk,
            'photo': user.photo.pk,
            'time_created': user.time_created
        })

    @staticmethod
    @csrf_exempt
    @require_http_methods(["DELETE"])
    def delete_user(request, user_pk):
        """
        Deletes a user by it's id (primary key)
        :param request: Http Request
        :return: None
        """
        User.objects.get(pk=user_pk).delete()
        return JsonResponse({'success': 'ok'})

    @staticmethod
    @csrf_exempt
    def get_random_user(request, user_pk):
        """
        get a random user
        :param request: the Get request
        :return: User
        """
        all_users = User.objects.exclude(pk=user_pk)
        random_user = random.choice(all_users)

        return UserView.get_user_json(request, random_user.pk)

    @staticmethod
    @csrf_exempt
    def get_friends(request, user_pk):
        """
        Get pk's of users who chat with a certain user

        :return: A list of users' pk's.
        :rtype: JsonResponse
        """

        users = []

        msg_list = Message.objects.all()

        # Add each pk the user is chatting with
        for message in msg_list:
            msg_receiver = message.receiver.pk
            msg_sender = message.sender.pk

            if (msg_sender == user_pk and
                    msg_receiver not in [user['user_pk'] for user in users]):

                users.append({'user_pk': msg_receiver,
                              'photo_pk': message.receiver.photo.pk})

            elif (msg_receiver == user_pk and
                  msg_sender not in [user['user_pk'] for user in users]):
                users.append({'user_pk': msg_sender,
                              'photo_pk': message.sender.photo.pk})

        users.sort(key=lambda user: user['user_pk'])
        return JsonResponse(users, safe=False)

    @staticmethod
    @csrf_exempt
    @require_http_methods(["POST"])
    def register(request):
        """
        On create - last_activated is the current time.

        :return: A json response containing new user's pk and its photo's pk
        :rtype: JsonResponse
        """

        body = json.loads(request.body)
        content = body['photo']

        img = Photo(
            base64=content,
            time_created=timezone.now()
        )
        img.save()

        new_user = User(
            photo=img,
            time_created=timezone.now(),
            last_active=timezone.now()
        )
        new_user.save()

        return JsonResponse({'user_pk': new_user.pk, 'photo_pk': img.pk})

    # @staticmethod
    # def update_last_active(request, pk_num):
    #     """
    #     Updating the last_active user attribute
    #     :param pk_num: int (id/pk number)
    #     :return: None
    #     """
    #     user = User.objects.get(pk=pk_num)
    #     user.last_active = timezone.now()


class PhotoView(View):
    """
    photo management
    """

    @staticmethod
    @csrf_exempt
    def get_all_images_html(request):
        all_photos = Photo.objects.all()
        return render(request, 'show_images.html', {'images': all_photos})

    @staticmethod
    def get_all_images_json(request):
        """
        :return: All users in a json
        :rtype: JsonResponse
        """
        all_photos = Photo.objects.all().values('base64', 'time_created', 'pk')
        return JsonResponse(list(all_photos), safe=False)

    @staticmethod
    def get_photo_html(request, photo_pk):
        photo = Photo.objects.get(pk=photo_pk)
        return render(request, 'detail.html', {
            'entity': 'Photo',
            'number': photo_pk,
            'time_created': photo.time_created,
            'photo_base64': photo.base64
        })

    @staticmethod
    def get_photo_json(request, img_pk):
        photo = Photo.objects.get(pk=img_pk)
        photo_json = {
            'base64': photo.base64,
            'time_created': photo.time_created,
            'pk': photo.pk
        }

        return JsonResponse(photo_json)

    @staticmethod
    @csrf_exempt
    @require_http_methods(["PUT"])
    def upload_img(request):
        img = Photo(
            base64=request.body.decode('utf-8'),
            time_created=timezone.now()
        )
        img.save()

        return JsonResponse({'success': 'ok'})

    @staticmethod
    @csrf_exempt
    @require_http_methods(["DELETE"])
    def delete_img(request, photo_pk):
        Photo.objects.filter(pk=photo_pk).delete()
        return JsonResponse({'success': 'ok'})


class MessageView(View):
    """
    messages management
    """

    @staticmethod
    @csrf_exempt
    @require_http_methods(['PUT'])
    def create_new_message(request):

        body_unicode = request.body
        body = json.loads(body_unicode)

        photo = None
        if 'photo_pk' in body:
            photo = Photo.objects.get(pk=int(body['photo_pk']))

        if not photo:
            msg = Message(
                sender=User.objects.get(pk=int(body['sender_pk'])),
                receiver=User.objects.get(pk=int(body['receiver_pk'])),
                content_text=body['content_text'],  # emojis...
                send_time=timezone.now()
            )
        else:
            msg = Message(
                sender=User.objects.get(pk=int(body['sender_pk'])),
                receiver=User.objects.get(pk=int(body['receiver_pk'])),
                content_text=body['content_text'],  # emojis...
                content_photo=photo,
                send_time=timezone.now()
            )
        msg.save()

        return JsonResponse({'success': 'ok'})

    @staticmethod
    def get_all_messages_json(request):
        messages = Message.objects.all().values('sender', 'receiver',
                                                'content_photo',
                                                'content_text', 'send_time')
        messages = list(messages)
        return JsonResponse(messages, safe=False)

    @staticmethod
    def get_message_json(request, msg_pk):
        msg = Message.objects.get(pk=msg_pk)
        return JsonResponse({
            'sender': msg.sender.pk,
            'receiver': msg.receiver.pk,
            'content_photo': msg.content_photo.pk,
            'content_text': msg.content_text,
            'send_time': msg.send_time
        })

    @staticmethod
    def get_conversation(request, user_id, friend_id):
        msg_list = Message.objects.filter(
            Q(sender=user_id, receiver=friend_id) |
            Q(sender=friend_id, receiver=user_id)
        ).order_by('send_time').values()

        return JsonResponse(list(msg_list), safe=False)
