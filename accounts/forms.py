from django import forms
from django.contrib.auth.forms import UserCreationForm
from mysite.models import PUser
from accounts.models import User
from crispy_forms.helper import FormHelper
from django.forms import SelectDateWidget

YEARS = [x for x in range(1940, 2011)]
YEARS.sort(reverse=True)

class RegistrationForm(UserCreationForm):

    username = forms.CharField(max_length=30)

    birthdate = forms.DateField(widget=SelectDateWidget(years=YEARS))

    class Meta:
        model = User
        fields = ("username", "name", "password1", "password2",)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)



        self.helper = FormHelper()
        self.helper.labels_uppercase = True
        self.helper.form_show_labels = True