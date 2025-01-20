from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import UserChangeForm,UserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email','username', )
    model = CustomUser
    add_form = UserCreationForm
    form = UserChangeForm

