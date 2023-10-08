from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext as _
from django.conf import settings

from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Submit

from wafer.registration.validators import validate_username
from wafer.users.models import UserProfile


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.include_media = False
        username = kwargs['instance'].username
        self.helper.form_action = reverse('wafer_user_edit',
                                          args=(username,))
        self.helper.add_input(Submit('submit', _('Save')))
        self.fields['first_name'].required = True
        self.fields['email'].required = True

    def clean_username(self):
        username = self.cleaned_data['username']
        validate_username(username)
        return username

    class Meta:
        # TODO: Password reset
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        pre_social_index = len(self.fields)

        # currently everything I'm asking for is an url, and this adds some
        # validation - we may need to revisit this later
        for field_name in settings.SOCIAL_MEDIA_ENTRIES:
            self.fields[field_name] = forms.URLField(max_length=1024)

        pre_code_index = len(self.fields)

        for field_name in settings.CODE_HOSTING_ENTRIES:
            self.fields[field_name] = forms.URLField(max_length=1024)

        self.helper = FormHelper(self)
        self.helper.include_media = False
        username = kwargs['instance'].user.username
        self.helper.form_action = reverse('wafer_user_edit_profile',
                                          args=(username,))

        # Add code hosting media header
        # We do this in this order to avoid needing to do
        # more maths
        if settings.CODE_HOSTING_ENTRIES:
            self.helper.layout.insert(pre_code_index, HTML('<p>Code</p>'))

        # Add social media header
        if settings.SOCIAL_MEDIA_ENTRIES:
            self.helper.layout.insert(pre_social_index, HTML('<p>Socail</p>'))


        self.helper.add_input(Submit('submit', _('Save')))

    class Meta:
        model = UserProfile
        exclude = ('user', 'kv')

