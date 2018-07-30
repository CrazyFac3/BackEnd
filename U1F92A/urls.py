from django.conf.urls import url
from django.http import JsonResponse
from django.urls import path

from . import views

urlpatterns = [
    # #########################################################################
    #                                   PHOTO                                 #
    # #########################################################################

    path(
        'photo/all',
        views.PhotoView.get_all_images_html,
    ),

    path(
        'photo/all/json',
        views.PhotoView.get_all_images_json,
    ),

    path(
        'photo/<int:photo_pk>/',
        views.PhotoView.get_photo_html,
    ),

    path(
        'photo/<int:img_pk>/json',
        views.PhotoView.get_photo_json,
    ),

    path(
        'photo/upload',
        views.PhotoView.upload_img,
    ),

    path(
        'photo/delete/<int:photo_pk>',
        views.PhotoView.delete_img,
    ),

    # #########################################################################
    #                                   MESSAGE                               #
    # #########################################################################

    path(
        'message/all/json',
        views.MessageView.get_all_messages_json,
    ),

    path(
        'message/create',
        views.MessageView.create_new_message,
    ),

    path(
        'message/<int:msg_pk>/json',
        views.MessageView.get_message_json,
    ),

    path(
        'message/conversation/<int:user_id>/<int:friend_id>',
        views.MessageView.get_conversation,
    ),

    # #########################################################################
    #                                    USER                                 #
    # #########################################################################

    path(
        'user/all/json',
        views.UserView.get_all_users_json,
    ),

    path(
        'user/<int:user_pk>/',
        views.UserView.get_user_html,
    ),

    path(
        'user/<int:user_pk>/json',
        views.UserView.get_user_json,
    ),

    path(
        'user/register/',
        views.UserView.register,
    ),

    path(
        'user/random/<int:user_pk>',
        views.UserView.get_random_user,
    ),

    path(
        'user/friends/<int:user_pk>',
        views.UserView.get_friends,
    ),

    path(
        'user/delete/<int:user_pk>',
        views.UserView.delete_user,
        name='delete_user'
    ),
]
