import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

###############################################################################
#                                  utils                                      #
###############################################################################


def asure_user(user, permission: str):
    """check if user is submitted and has permission"""
    if not user:
        raise ValueError('user is not submitted')
    if permission == "user":
        pass
    elif permission == "staff":
        if not user.is_staff:
            raise ValueError('user is not a staff member')
    elif permission == "superuser":
        if not user.is_superuser:
            raise ValueError('user is not a superuser')


def asure_string(string: str, min_length: int = 0):
    """check if string is submitted"""
    if not string:
        raise ValueError('string is not submitted')
    if len(string) < min_length:
        raise ValueError('string is too short')


def asure_boolean(boolean):
    """check if boolean is submitted"""
    if not boolean:
        raise ValueError('boolean is not submitted')
    if not isinstance(boolean, bool):
        raise ValueError('boolean is not a boolean')


###############################################################################
#                                BaseEntity                                   #
###############################################################################


class BaseEntityManager(models.Manager):
    """
    Base manager for all entities.
    """

    def get_queryset(self, **kwargs):
        """
        Returns a queryset of all entities.
        """
        return self.get_queryset().filter(**kwargs)


class BaseEntity(models.Model):
    """
    Base class for all models
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def soft_delete(self):
        self.active = False
        self.save()

    class Meta:
        abstract = True


###############################################################################
#                                  User                                       #
###############################################################################


class UserManager(BaseUserManager):
    """
    Custom user manager.
    """

    def create_user(self, password=None, **extra_fields):
        """Creates and saves a new user"""

        if extra_fields.get('name') is None:
            raise ValueError('The given name must not be undefined')
        if len(extra_fields.get('name')) < 5:
            raise ValueError(
                'The given name must be at least 5 characters long')
        if password is None:
            raise ValueError('The given password must not be undefined')
        if len(password) < 8:
            raise ValueError(
                'The given password must be at least 8 characters long')

        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staff_user(self, password=None, **extra_fields):
        """Creates and saves a new staff user"""
        user = self.create_user(password, **extra_fields)
        user.is_staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self, password=None, **extra_fields):
        """Creates and saves a new superuser"""
        user = self.create_user(password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin, BaseEntity):
    """
    Custom user model.
    """
    name = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    elo = models.IntegerField(default=1000)

    objects = UserManager()

    USERNAME_FIELD = 'name'

    def __str__(self):
        return f"user object {self.name}"
