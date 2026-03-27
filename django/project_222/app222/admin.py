from django.contrib import admin
from .models import User


class UserAdminView(admin.ModelAdmin):
    list_display = ('id', 'surname','name', 'birthdate')


admin.site.register(User, UserAdminView)