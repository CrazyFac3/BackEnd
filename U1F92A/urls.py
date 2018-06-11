from django.http import JsonResponse
from django.urls import path

from . import views

urlpatterns = [
    # /U1F92A/
    path('', views.index, name='index'),

    # /U1F92A/Photo/  --> displays all the photos. press to get more info.
    path(
        'photo/',
        views.PhotoView.display_all_photos,
        name="display_all_photos"
    ),

    # /U1F92A/Photo/325/  --> displays info about a specific photo.
    path(
        'photo/<int:photo_pk>/',
        views.PhotoView.details_photo,
        name="details_photo"
    ),

    # /U1F92A/User/user_pk/
    path(
        'user/<int:user_pk>/',
        views.UserView.display_user,
        name="display_user"
    ),

    # /U1F92A/Users/  --> gives all users in a json.
    path(
        'users/',
        views.UserView.get_all_users,
        name="get_all_users"
    ),

    # /U1F92A/User/GetJson/user_pk/
    path(
        'user/get_json/<int:pk_num>/',
        lambda request, pk_num: JsonResponse(
            views.UserView.get_user_json(request, pk_num)),
        name="get_user"
    ),

    # /U1F92A/User/Register/
    path(
        'user/register/',
        views.UserView.register,
        name="register"
    ),

    # /U1F92A/Photo/UploadImg/
    path(
        'photo/upload_img/',
        views.PhotoView.upload_img,
        name="upload_img"
    ),

    # /U1F92A/user/random
    path(
        'user/random',
        views.UserView.get_random_user,
        name="get_random_user"
    ),

    # /U1F92A/user/friends
    path(
        'user/friends',
        views.UserView.get_friends,
        name="get_friends"
    ),

    # /U1F92A/GetPhotoJson/<photo_pk>/
    path(
        'get_photo_json/<int:img_pk>/',
        lambda request, img_pk: JsonResponse(
            views.PhotoView.get_photo(request, img_pk)),
        name="get_photo"
    ),

    # /U1F92A/Photos
    path(
        'photos/',
        views.PhotoView.get_all_images,
        name="get_all_images"
    ),

    # /U1F92A/Messages/
    path(
        'messages/',
        views.MessageView.get_all_messages,
        name="get_all_messages"
    ),

    # /U1F92A/CreateMessage/
    path(
        'create_message/',
        views.MessageView.create_new_message,
        name="create_new_message"
    ),

    # U1F92A/GetMessage/
    path(
        'get_message/',
        views.MessageView.get_message,
        name="get_message"
    ),

    # U1F92A/GetConversation/
    path(
        'get_conversation/',
        views.MessageView.get_messages,
        name="get_messages"
    )
]
