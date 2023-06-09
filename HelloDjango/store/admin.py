from django.contrib import admin
from .models import Book, Genre, Author, Favorite, Comment, Position, Employee,\
    Test
from user_api.models import MyUser, Profile

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Profile)
admin.site.register(Author)
admin.site.register(Favorite)
admin.site.register(Comment)
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(Test)


class MyUserAdmin(admin.ModelAdmin):
    list_filter = ['is_staff', 'is_superuser']


admin.site.register(MyUser,MyUserAdmin)
