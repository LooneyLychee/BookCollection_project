from django import forms
from .models import Profile


class ProfileModelForm(forms.ModelForm):
    image = forms.FileField(required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'avatar')

    def __init__(self, *args, **kwargs):
        super(ProfileModelForm, self).__init__(*args, **kwargs)

        self.fields['avatar'].required = False
