from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import *
from django.utils import timezone


def index(request):
    return HttpResponse("Hello, world. You're at polls index.")


class UserView(View):

    @staticmethod
    def register(uphoto):
        """
        on create - last_activated is the current time.
        :param uphoto: Photo (U1F92A.models)
        :return: None
        """
        # upload_img(uphoto)
        new_user = User(photo=uphoto, time_created=timezone.now(), last_active=timezone.now())
        new_user.save()

    @staticmethod
    def update_last_active(pk_num):
        """
        updating the last_active user attribute
        :param pk_num: int (id/pk number)
        :return: None
        """
        user = User.objects.get(pk=pk_num)
        user.last_active = timezone.now()

    @staticmethod
    def get_all_users():
        """
        Returning all users list
        :return: list
        """
        return User.objects.all()


