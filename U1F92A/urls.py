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

    # /U1F92A/Photo/img_url/  --> upload a new image to the database.
    path(
        'Photo/<path:photo_url>',
        views.PhotoView.upload_img,
        name="upload_img"
    ),

    # /U1F92A/User/  --> gives all users in a json.
    path(
        'User/',
        views.UserView.get_all_users,
        name="get_all_users"
    ),

]
