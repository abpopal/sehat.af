from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator

usename_regex = RegexValidator(regex='^[a-zA-Z]+$', message="Username should be combination of alphabet", code='ValueError')


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have an username address')

        user = self.model(
            username= username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, password):

        user = self.create_user(
            username,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name_regex = RegexValidator(regex='^[a-zA-Z ]+$', message="Name cannot include numbers", code='ValueError')

    username = models.CharField(validators=[usename_regex], max_length=30, unique=True, verbose_name="UserName")
    name = models.CharField(max_length=30, validators=[name_regex])
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    approved = models.BooleanField(default=True)
    ishospital = models.BooleanField(default=False)
    isdonor = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        #"Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        #"Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def make_donor(self):
        self.isdonor = True
        return None

    @property
    def is_staff(self):
        #"Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        #"Is the user a admin member?"
        return self.admin 

    @property
    def is_active(self):
        #"Is the user active?"
        return self.active

    @property
    def is_hospital(self):
        # "Is the user hospital?"
        return self.ishospital

    @property
    def is_donor(self):
        return self.isdonor


