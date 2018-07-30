from django.conf.urls import url
from django.http import JsonResponse
from django.urls import path

from . import views

urlpatterns = [
    # /U1F92A/
    # path('', views.index, name='index'),

    # #########################################################################
    #                                   PHOTO                                 #
    # #########################################################################

    # GET /U1F92A/Photo/  --> displays all the photos. press to get more info.
    path(
        'photo/all',
        views.PhotoView.get_all_images_html,
    ),

    path(
        'photo/all/json',
        views.PhotoView.get_all_images_json,
    ),

    # /U1F92A/Photo/325/  --> displays info about a specific photo.
    path(
        'photo/<int:photo_pk>/',
        views.PhotoView.get_photo_html,
    ),

    # /U1F92A/GetPhotoJson/<photo_pk>/
    path(
        'photo/<int:img_pk>/json',
        views.PhotoView.get_photo_json,
    ),

    # /U1F92A/Photo/UploadImg/
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

    # /U1F92A/Messages/
    path(
        'message/all/json',
        views.MessageView.get_all_messages_json,
    ),

    # /U1F92A/CreateMessage/
    path(
        'message/create',
        views.MessageView.create_new_message,
    ),

    # U1F92A/GetMessage/
    path(
        'message/<int:msg_pk>/json',
        views.MessageView.get_message_json,
    ),

    # U1F92A/GetConversation/
    path(
        'message/conversation/<int:user_id>/<int:friend_id>',
        views.MessageView.get_conversation,
    ),

    # #########################################################################
    #                                    USER                                 #
    # #########################################################################

    # /U1F92A/Users/  --> gives all users in a json.
    path(
        'user/all/json',
        views.UserView.get_all_users_json,
    ),

    # /U1F92A/User/user_pk/
    path(
        'user/<int:user_pk>/',
        views.UserView.get_user_html,
    ),

    # /U1F92A/User/GetJson/user_pk/
    path(
        'user/<int:user_pk>/json',
        views.UserView.get_user_json,
    ),

    # /U1F92A/User/Register/
    path(
        'user/register/',
        views.UserView.register,
    ),

    # /U1F92A/user/random
    path(
        'user/random/<int:user_pk>',
        views.UserView.get_random_user,
    ),

    # /U1F92A/user/friends
    path(
        'user/friends/<int:user_pk>',
        views.UserView.get_friends,
    ),

    # U1F92A/delete_user/ ---> Parameters: user_pk (int)
    path(
        'user/delete/<int:user_pk>',
        views.UserView.delete_user,
        name='delete_user'
    ),
]
