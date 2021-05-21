from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import PUser, Hospital, Donor, Blood_Records
from django.core.validators import RegexValidator
from django.forms import SelectDateWidget
from mysite.models import Blood_Records
from crispy_forms.helper import FormHelper

YEARS = [x for x in range(1940, 2011)]
YEARS.sort(reverse=True)

name_regex = RegexValidator(regex='^[a-zA-Z ]+$', message="Name cannot include numbers", code='ValueError')

gender = [('male', "Male"), ('female', "Female")]
class EditProfileForm(forms.ModelForm):


    template_name ='/templates/profile'



    class Meta:
        model = PUser

        fields = (
            'name',
            'contact',
            'contact',
            'Email',
            'loc_id',
            'gender',
            'birthdate',

        )
        widgets = {
            'birthdate': SelectDateWidget(years=YEARS),
            'gender': forms.Select(choices=(gender))
        }


class EditHospitalProfileForm(forms.ModelForm):

    template_name ='/templates/profile'

    class Meta:
        model = Hospital

        fields = (
            'name',
            'Email',
            'contact',
            'loc_id',

        )

class DonorRegistrationForm(forms.ModelForm):
    template_name ='/templates/donorform'

    class Meta:
        model = Donor

        fields = (
            'bg_id',

        )


class AddRecordForm(forms.ModelForm):
    enumerate_name ='/templates/add_record'

    class Meta:
        model = Blood_Records

        fields = (
            'quantity',
            'exp_date',
            'b_charges',
            'bg_id',

        )