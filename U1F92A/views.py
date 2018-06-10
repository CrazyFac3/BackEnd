import json
import random
from django.views import View
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse, HttpResponseServerError, \
    HttpResponseBadRequest


from .models import *


def index(request):
    return HttpResponse("Home Page")


class UserView(View):
    """
    user management
    """

    @csrf_exempt
    @require_http_methods(["GET", "POST"])
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

    @staticmethod
    def display_user(request, user_pk):
        user = User.objects.get(pk=user_pk)

        return HttpResponse(
            "<h2>Details for User number: {0}.<br>"
            "Date created: {1}</h2><br>"
            '<img src="{2}"/>.'.format(user_pk, user.time_created,
                                       user.photo.base64)
        )

    @staticmethod
    def update_last_active(request, pk_num):
        """
        Updating the last_active user attribute
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

        users = User.objects.all().values('photo', 'time_created', 'pk')
        users = list(users)
        response = JsonResponse(users, safe=False)

        return response

    @staticmethod
    def get_user_json(request, pk_num):
        user = User.objects.get(pk=pk_num)
        user_json = {
            'photo': user.photo.pk,
            'time_created': user.time_created,
            'pk': user.pk
        }

        return user_json

    @staticmethod
    @csrf_exempt
    def get_random_user(request):
        """
        get a random user
        :param request: the Get request
        :return: User
        """
        if not request.GET.get('user_pk'):
            return HttpResponseBadRequest('Bad Request! the url must contain '
                                          'a query parameter of user_pk!')
        try:
            user_pk = int(request.GET.get('user_pk'))
        except ValueError:
            return HttpResponseBadRequest(
                'Bad Request! user_pk must be an integer!')

        all_users = User.objects.all()
        random_user = random.choice(all_users)
        attempts = 10  # Number of attempts to find a user
        while random_user.pk == user_pk and attempts != 0:
            random_user = random.choice(all_users)
            attempts -= 1

        if attempts == 0:
            # In case tried and did not manage to find a random user
            # Return a user with pk = 0, which means not found
            return JsonResponse({'photo': '',
                                 'time_created': str(timezone.now()),
                                 'pk': 0})
        else:
            return JsonResponse(
                UserView.get_user_json(request, random_user.pk))


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
            str(PhotoView.get_photo(request, photo_pk)["time_created"]) +
            ".</h2>"
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

        photo = None
        if 'photo_pk' in body.keys():
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

        return HttpResponse("Created!")

    @staticmethod
    def get_all_messages(request):
        messages = Message.objects.all().values('sender', 'receiver',
                                                'content_photo',
                                                'content_text', 'send_time')
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
        user_id = int(params['user_id'])
        friend_id = int(params['friend_id'])

        msg_list = Message.objects.all().values('sender',
                                                'receiver',
                                                'content_photo',
                                                'content_text',
                                                'send_time',
                                                'id')

        msgs_list_final = []

        # Each user is either sender or receiver
        for message in msg_list:
            if (user_id == int(message['sender']) and friend_id == int(
                    message['receiver'])) or (
                    user_id == int(message['receiver']) and friend_id == int(
                    message['sender'])):
                msgs_list_final.append(message)

        msgs_dict = {
            key: value for key, value in enumerate(msgs_list_final, 1)
        }

        response = JsonResponse(msgs_dict, safe=False)

        return response
