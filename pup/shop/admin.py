from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import category, Product ,CustomUser, BusinessUser, Cart


class CustomUserInline(admin.StackedInline):
    model = CustomUser
    can_delete: False
    verbose_name_plural = 'CustomUsers'

class CustomizedUseradmin(UserAdmin):
    inlines = (CustomUserInline, )


admin.site.register(category)
admin.site.register(Product)
admin.site.unregister(User)
admin.site.register(User, CustomizedUseradmin)
admin.site.register(CustomUser)
admin.site.register(BusinessUser)
admin.site.register(Cart)




