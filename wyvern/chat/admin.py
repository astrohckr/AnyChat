# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.admin.utils import display_for_field
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Category, Group


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
    ]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['category']}),
    ]
    list_display = ('name', 'category')

# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Group, GroupAdmin)

#
# class GroupChangeForm(admin.ModelAdmin):
#     class Meta(UserChangeForm.Meta):
#         model = Group
#
#
# class MyUserCreationForm(UserCreationForm):
#     error_message = UserCreationForm.error_messages.update({
#         'duplicate_username': 'This username has already been taken.'
#     })
#
#     class Meta(UserCreationForm.Meta):
#         model = User
#
#     def clean_username(self):
#         username = self.cleaned_data["username"]
#         try:
#             User.objects.get(username=username)
#         except User.DoesNotExist:
#             return username
#         raise forms.ValidationError(self.error_messages['duplicate_username'])
#
# @admin.register(User)
# class UserAdmin(AuthUserAdmin):
#     form = MyUserChangeForm
#     add_form = MyUserCreationForm
