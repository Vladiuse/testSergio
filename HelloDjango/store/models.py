from django.db import models
import os
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.models import BaseUserManager, UserManager
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from user_api.models import MyUser, Profile
#
# class MyUserManager(UserManager):
#
#     def create_user(self, *args, **kwargs):
#         user = super().create_user(*args, **kwargs)
#         Profile.objects.create(
#             owner=user,
#         )
#         return user
#
#     def create_superuser(self, *args, **kwargs):
#         user = super().create_superuser(*args, **kwargs)
#         Profile.objects.create(owner=user)
#         return user
#
#
# class MyUser(AbstractUser):
#     objects = MyUserManager()
#
#
# class Profile(models.Model):
#     NO_SEX = 'no_sex'
#     MAN = 'man'
#     WOMAN = 'woman'
#
#     SEX_CHOICE = [
#         (MAN, 'Мужской'),
#         (WOMAN, 'Женский'),
#     ]
#
#     owner = models.OneToOneField(
#         MyUser,
#         primary_key=True,
#         on_delete=models.CASCADE,
#     )
#     first_name = models.CharField(
#         blank=True,
#         max_length=50,
#     )
#     last_name = models.CharField(
#         blank=True,
#         max_length=50,
#     )
#     age = models.PositiveIntegerField(
#         blank=True,
#         null=True,
#         validators=[MinValueValidator(13), MaxValueValidator(120)],
#     )
#     sex = models.CharField(
#         max_length=6,
#         blank=True,
#         choices=SEX_CHOICE,
#         default=NO_SEX,
#     )
#     address = models.CharField(
#         max_length=150,
#         blank=True,
#     )
#
#     def delete(self, **kwargs):
#         raise ZeroDivisionError
#
#     def __str__(self):
#         return f'{self.pk} {self.user.username}: {self.first_name}'
#

class Position(models.Model):
    id = models.CharField(
        max_length=30,
        unique=True,
        primary_key=True,
    )
    name = models.CharField(
        max_length=30,
        unique=True,
    )

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
    )
    date_joined = models.DateField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.user}:{self.position}'



class Author(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class BookManager(models.Manager):

    def get_queryset(self):
        return Book.objects.filter(is_public=True)


class Book(models.Model):
    name = models.CharField(
        max_length=30
    )
    price = models.FloatField(
        default=0
    )
    genre = models.ManyToManyField(
        'Genre',
        blank=True
    )
    image = models.ImageField(
        upload_to='book_images',
        blank=True
    )
    is_public = models.BooleanField(
        default=True
    )
    description = models.TextField(
        blank=True
    )
    author = models.ForeignKey(
        Author,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    available_in_store = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['pk',]

    def __str__(self):
        return self.name

    def delete(self):
        if self.image:
            os.remove(self.image.path)
        super().delete()

    def comments_count(self):
        return self.comment.count()

    # def add_to_favorite(self, user):



class Comment(models.Model):
    owner = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='comment',
    )
    text = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True,
    )
    stars = models.PositiveIntegerField(
        validators=[MaxValueValidator(5),]
    )

    class Meta:
        unique_together = ['owner', 'book']

    def __str__(self):
        return f'<Comment:{self.pk}> {self.owner} {self.book.pk}:{self.book}'


class Genre(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True
    )

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='favorite',
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='is_favorite',
    )


    class Meta:
        unique_together = ['user', 'book']


    def __str__(self):
        return f'{self.user}:{self.book}'


class Test(models.Model):
    name = models.CharField(max_length=20)
