from django import forms
from django.core.validators import FileExtensionValidator

from testapp.models import SMS, Img


class SMSCreateForm(forms.ModelForm):
    class Meta:
        model = SMS
        fields = ('sender', 'receiver', 'comment',)


class ImgForm(forms.ModelForm):
    img = forms.ImageField(label='Изображение', validators=[FileExtensionValidator(allowed_extensions=('pdf', 'jpg', 'png'))],
                           error_messages={'invalid_extension': 'Данный формат не поддерживается!'})

    desc = forms.CharField(label='Описание', widget=forms.widgets.Textarea())

    class Meta:
        model = Img
        fields = '__all__'
