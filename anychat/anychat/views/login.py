# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from uuid import uuid4
from PIL.OleFileIO import long
from django.http.response import HttpResponse
from anychat.anychat.models import User, Point
from anychat.anychat.utils import is_valid_uuid


def login(request):
    '''
    Create a new user or add the existing user to the session.

    Logged in users are kept in the session.
    This is called when a user has no session.

    Users are also kept in the database and can be looked up by a user_id the user keeps in long term storage in the
    case that the session ends.

    Each login will also update the users' coordinates.
    '''

    user_id = request.POST['userId']
    longitude = request.POST['lon']
    latitude = request.POST['lat']

    user = None

    # create the point
    point = Point()
    point.latitude = latitude
    point.longitude = longitude
    point.save()

    # get or create the user
    if is_valid_uuid(user_id):
        user_query = User.objects.filter(uuid=user_id)

        if user_query.count() > 0:
            user = user_query.get()

    if not user:
        user = User()

    # set the new point
    user.uuid = uuid4()  # generate a new uuid every login
    user.point = point
    user.save()

    request.session['user'] = {'pk': user.pk, 'uuid': str(user.uuid)}

    # this one may not be necessary, but it may be better to keep this in the session as well
    request.session['point'] = {'pk': point.pk, 'longitude': point.longitude, 'latitude': point.latitude}

    return HttpResponse(user.uuid)
