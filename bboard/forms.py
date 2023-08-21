from django.core.exceptions import ValidationError
from django.forms import ModelForm, modelform_factory, DecimalField
from django.forms.widgets import Select
from django.core import validators
from django import forms

from bboard.models import Bb, Rubric


# class BbForm(ModelForm):
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')


# BbForm = modelform_factory(Bb,
#                            fields=('title', 'content', 'price', 'rubric'),
#                            labels={'title': 'Название товара'},
#                            help_texts={'rubric': 'He забудьте выбрать рубрику!'},
#                            field_classes={'price': DecimalField},
#                            widgets={'rubric': Select(attrs={'size': 8})})


class BbForm(ModelForm):
    title = forms.CharField(label='Название товара',
                            validators=[validators.RegexValidator(regex='^.{4,}$')],
                            error_messages={'invalid': 'Слишком короткое название товара!'})
    content = forms.CharField(label='Описание',
                              widget=forms.widgets.Textarea())
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Рубрика', help_text='Не забудьте выбрать рубрику!',
                                    widget=forms.widgets.Select(attrs={'size': 5,
                                                                       'class': 'danger'}))

    def clean_title(self):
        val = self.cleaned_data['title']
        if val == "Прошлогодний снег":
            raise ValidationError(f"Товар: {self.cleaned_data['title']} к продаже не допускается")
        return val

    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data['content']:
            errors['content'] = ValidationError('Укажите описание продаваемого товара')
        if self.cleaned_data['price'] <= 0:
            errors['price'] = ValidationError('Укажите положительное значение')

        if errors:
            raise ValidationError(errors)

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
