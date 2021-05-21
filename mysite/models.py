from django.db import models
from accounts.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# Create your models here.

name_regex = RegexValidator(regex='^[a-zA-Z ]+$', message="Name cannot include numbers", code='ValueError')


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def validate_email(email):
    afterAt = email.split("@")[-1]
    postafter = afterAt.split('.')
    if len(postafter) == 2 and not hasNumbers(postafter):
        print("email is .com valid")
    elif len(postafter) == 3 and not hasNumbers(postafter):
        print("email is .edu.af valid")
    else:
        raise ValidationError(
            _('%(value)s is not a valid email'),
            params={'value': email},
        )

class Blood_Group(models.Model):
    bg_Id = models.AutoField(primary_key=True)
    bg_name = models.CharField(max_length=10)

    objects = models.Manager()

    def __str__(self):  # __unicode__ on Python 2
        return self.bg_name


class Location(models.Model):
    loc_id = models.AutoField(primary_key=True)
    loc_name = models.CharField(max_length=30)
    objects = models.Manager()
    def __str__(self):  # __unicode__ on Python 2
        return self.loc_name

class Hospital(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$',
                                 message="Phone number must be entered in the format: '+999999999'.")

    h_id = models.AutoField(primary_key=True)
    loc_id = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(validators=[name_regex], max_length=30)
    h_username = models.OneToOneField(User, on_delete=models.CASCADE)
    Email = models.EmailField(validators=[validate_email])
    rating = models.FloatField()

    contact = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list

    objects = models.Manager()


class Blood_Bank(models.Model):
    bb_id = models.AutoField(primary_key=True)
    h_id = models.ForeignKey(Hospital, null=True, blank=True, on_delete=models.CASCADE)
    objects = models.Manager()



class PUser(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$',
                                 message="Phone number must be entered in the format: '+999999999'.")
    email_regex = RegexValidator(regex=r"\b[\w.-]+@[\w.-]+.\w{2,4}\b", message="invalid email")
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(validators=[name_regex], max_length=30)
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(validators=[phone_regex],
                               max_length=17, blank=True)  # validators should be a list
    Email = models.EmailField(validators=[validate_email])
    loc_id = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    birthdate = models.DateField()
    gender = models.CharField(max_length=10)

    objects = models.Manager()

class Donor(models.Model):
    d_id = models.AutoField(primary_key=True)
    bg_id = models.ForeignKey(Blood_Group, null=True, blank=True, on_delete=models.SET_NULL)
    user_id = models.OneToOneField(PUser, null=True, blank=True, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    objects = models.Manager()


class Blood_Records(models.Model):
    objects = models.Manager()
    record_id = models.AutoField(primary_key=True)
    quantity = models.IntegerField(null=True,  blank=True,)
    exp_date = models.DateField(null=True,  blank=True,)
    b_charges = models.IntegerField(null=True,  blank=True,)
    bg_id = models.ForeignKey(Blood_Group, null=False,  blank=False, on_delete=models.CASCADE)
    bb_id = models.ForeignKey(Blood_Bank, null=True, blank=True, on_delete=models.SET_NULL)
    d_id = models.OneToOneField(Donor, null=True, blank=True, on_delete=models.CASCADE)

class Requests(models.Model):
    req_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, default="Pending")
    remarks = models.TextField()
    record_id = models.ForeignKey(Blood_Records, null=True, blank=True, on_delete=models.SET_NULL)
    objects = models.Manager()

    @classmethod
    def create(cls, recordid):
        request = cls(record_id=recordid)
        return request

class User_Requests(models.Model):
    req_id = models.ForeignKey(Requests, null=True, blank=True, on_delete=models.CASCADE)
    user_id = models.ForeignKey(PUser, null=False, blank=False, on_delete=models.CASCADE)
    r_date = models.DateField(default=datetime.date.today)
    objects = models.Manager()

    @classmethod
    def create(cls, reqid):
        request = cls(req_id=reqid)


        return request

