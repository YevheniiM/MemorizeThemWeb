from django.shortcuts import redirect
from .core import contacts as cont
from .core import quickstart
from models_test.models import Contact
from django.contrib import auth
import os


def login(request):
    c = quickstart.Connections()
    users = c.get_all_data()
    contacts = cont.Contacts(users).contacts

    for contact in contacts:
        try:
            user = Contact.objects.get(id=contact.ID, owner_id=auth.get_user(request).id)
        except Contact.DoesNotExist:
            user = ''

        if not user:
            con = Contact()
            con.id = contact.ID
            con.owner_id = auth.get_user(request).id
            con.name = contact.name
            con.email = contact.email
            con.mobile_phone = contact.phone_number.get('phone', '')
            con.photo = contact.photos
            con.save()

    c.del_credentials()

    return redirect('/contacts/')
