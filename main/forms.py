from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Client, Message, Mailing

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class MailingForm(forms.ModelForm):
    PERIODICITY_CHOICES = [
        ('1 min', 'Once a minute'),
        ('daily', 'Once a day'),
        ('weekly', 'Once a week'),
        ('monthly', 'Once a month'),
    ]

    periodicity = forms.ChoiceField(choices=PERIODICITY_CHOICES, initial='daily',
                                    widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Mailing
        exclude = ['status', 'owner']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

        # Установка начального значения для поля periodicity
        self.fields['periodicity'].initial = 'daily'
