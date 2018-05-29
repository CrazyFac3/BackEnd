from django.http import JsonResponse
from django.urls import path
from . import views

urlpatterns = [
    # /U1F92A/
    path('', views.index, name='index'),

    # /U1F92A/Photo/  --> displays all the photos. press to get more info.
    path(
        'Photo/',
        views.PhotoView.display_all_photos,
        name="display_all_photos"
    ),

    # /U1F92A/Photo/325/  --> displays info about a specific photo.
    path(
        'Photo/<int:photo_pk>/',
        views.PhotoView.details_photo,
        name="details_photo"
    ),

    # /U1F92A/Photo/photo_base64  --> upload a new image to the database.
    # path(
    #     'Photo/<path:photo_base64>',
    #     views.PhotoView.upload_img,
    #     name="upload_img"
    # ),

    # /U1F92A/User/Register/photo_base64
    path(
        'User/Register/<path:photo_base64>',
        views.UserView.register,
        name="register"
    ),

    # /U1F92A/User/user_pk/
    path(
        'User/<int:user_pk>/',
        views.UserView.display_user,
        name="display_user"
    ),

    # /U1F92A/User/  --> gives all users in a json.
    path(
        'Users/',
        views.UserView.get_all_users,
        name="get_all_users"
    ),

    # /U1F92A/User/GetJson/user_pk/
    path(
        'User/GetJson/<int:pk_num>/',
        lambda request, pk_num: JsonResponse(views.UserView.get_user_json(request, pk_num)),
        name="get_user"
    ),

    # /U1F92A/User/RegisterJson/
    path(
        'User/RegisterJson/',
        views.UserView.register_with_json,
        name="register_with_json"

    ),

    # /U1F92A/Photo/UploadImg/
    path(
        'Photo/UploadImg/',
        views.PhotoView.upload_img,
        name="upload_img"
    ),

    # /U1F92A/User/Random/
    path(
        'User/Random/',
        views.UserView.get_random_user,
        name="get_random_user"
    ),

    # /U1F92A/GetPhotoJson/<photo_pk>/
    path(
        'GetPhotoJson/<int:img_pk>/',
        lambda request, img_pk: JsonResponse(views.PhotoView.get_photo(request, img_pk)),
        name="get_photo"
    ),

    # /U1F92A/Photos
    path(
        'Photos/',
        views.PhotoView.get_all_images,
        name="get_all_images"
    ),

    # /U1F92A/Messages/
    path(
        'Messages/',
        views.MessageView.get_all_messages,
        name="get_all_messages"
    ),

    # /U1F92A/CreateMessage/
    path(
        'CreateMessage/',
        views.MessageView.create_new_message,
        name="create_new_message"
    ),

    #U1F92A/GetMessage/
    path(
        'GetMessage/',
        views.MessageView.get_message,
        name="get_message"
    )


]
