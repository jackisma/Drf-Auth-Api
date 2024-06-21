from tkinter import N
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Using BaseUserManager, AbstractBaseUser Classes To Create And Use Django Custom User Model 

# User Manager Class That Does The User and Super User Creation Operations  
class MyUserManager(BaseUserManager):
    def create_user(self, email,name,remember_me ,password=None,password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name = name ,
            remember_me = remember_me 
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, remember_me , password=None, password2=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name = name ,
            remember_me = remember_me

        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    




# Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    remember_me = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name","remember_me"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin